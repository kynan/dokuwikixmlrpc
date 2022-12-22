#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# TODO
# allow to overwrite useragent?

"""DokuWiki XMLRPC module.

This modules allows to interact with the XML-RPC interface of DokuWiki
instances. It supports all methods of the DokuWiki XML-RPC interface.
"""

from __future__ import print_function
from functools import wraps
# Python 2 imports
try:
    from urllib import urlencode
    from urllib2 import urlopen
    from urllib2 import URLError
    import xmlrpclib
# Python 3 imports
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import URLError
    import xmlrpc.client as xmlrpclib
from xml.parsers.expat import ExpatError

__version__ = '2022.12.22'
__author__ = 'Michael Klier <chi@chimeric.de>'
__maintainer__ = 'Florian Rathgeber'


class DokuWikiError(Exception):
    """DokuWikiError base class."""
    pass


class DokuWikiXMLRPCError(DokuWikiError):
    """Triggered on XMLRPC faults."""

    def __init__(self, obj):
        """Initalize and call anchestor __init__()."""
        DokuWikiError.__init__(self)
        if isinstance(obj, xmlrpclib.Fault):
            self.page_id = obj.faultCode
            self.message = obj.faultString
        else:
            self.page_id = 0
            self.message = obj

    def __str__(self):
        """Format returned error message."""
        return '<%s %s: \'%s\'>' % (self.__class__.__name__,
                                    self.page_id,
                                    self.message)


class DokuWikiXMLRPCProtocolError(DokuWikiError):
    """Triggered on XMLRPC protocol faults."""

    def __init__(self, obj):
        """Initalize and call anchestor __init__()."""
        DokuWikiError.__init__(self)
        self.url = obj.url
        self.errcode = obj.errcode
        self.errmsg = obj.errmsg

    def __str__(self):
        """Format returned error message."""
        return '<%s %s: \'%s\' at %s>' % (self.__class__.__name__,
                                          self.errcode, self.errmsg, self.url)


class DokuWikiURLError(DokuWikiError):
    """Triggered when the URL supplied to DokuWikiClient is not
    valid/reachable."""

    def __init__(self, url):
        """Initalize and call anchestor __init__()."""
        DokuWikiError.__init__(self)
        self.message = url

    def __str__(self):
        """Format returned error message."""
        return '%s: Could not connect to <%s>' % (self.__class__.__name__,
                                                  self.message)


def checkerr(f):
    """Decorator that calls the given function and catches
    :class:`xmlrpclib.Fault` exceptions."""
    @wraps(f)
    def catch_xmlerror(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except xmlrpclib.Fault as fault:
            raise DokuWikiXMLRPCError(fault)
        except xmlrpclib.ProtocolError as fault:
            raise DokuWikiXMLRPCProtocolError(fault)
        # An ExpatError is raised if xmlrpclib cannot parse the response e.g.
        # because it is not valid XML. DokuWiki sends the plain text response
        # "XML-RPC server not enabled" if the XML RPC interface is not enabled.
        except ExpatError:
            raise DokuWikiError('Failed to parse response. Is the DokuWiki XML-RPC server enabled?')
    return catch_xmlerror


class DokuWikiClient(object):
    """DokuWiki XML-RPC client.

    This class implements a client for DokuWikis XML-RPC interface. All methods
    return exactly the data returned by DokuWikis XML-RPC interface. If
    something goes wrong a method raises a DokuWikiXMLRPCError which contains
    information reported by the XML-RCP interface.
    """

    def __init__(self, url, user, passwd, http_basic_auth=False, timeout=10,
                 context=None):
        """Create DokuWiki XMLRPC client.

        Try to get a XML-RPC object. If this step fails a DokuWIKIXMLRPCError
        is raised. If the supplied URL is not reachable we raise a
        DokuWikiURLError. Use these to catch bad user input.
        """

        self._url = url
        self._user = user
        self._passwd = passwd
        self._http_basic_auth = http_basic_auth
        self._timeout = timeout
        self._context = context
        self._user_agent = ' '.join(['DokuWikiXMLRPC ',
                                     __version__,
                                     '(https://github.com/kynan/dokuwikixmlrpc)'])

        self._xmlrpc = self._xmlrpc_init()

    @checkerr
    def _xmlrpc_init(self):
        """Initialize the XMLRPC object."""
        script = '/lib/exe/xmlrpc.php'

        try:
            urlopen(self._url + script, timeout=self._timeout)
        except (ValueError, URLError):
            raise DokuWikiURLError(self._url)

        if self._http_basic_auth:
            proto, url = self._url.split('://')
            url = ''.join([proto, '://', self._user, ':', self._passwd, '@',
                           url, script])
        else:
            url = ''.join([self._url, script, '?',
                           urlencode({'u': self._user, 'p': self._passwd})])

        xmlrpclib.Transport.user_agent = self._user_agent
        xmlrpclib.SafeTransport.user_agent = self._user_agent

        return xmlrpclib.ServerProxy(url, context=self._context)

    @property
    @checkerr
    def dokuwiki_version(self):
        """DokuWiki version reported by the remote Wiki."""
        return self._xmlrpc.dokuwiki.getVersion()

    @checkerr
    def rpc_version_supported(self):
        """Return the supported RPC version reported by the remote Wiki."""
        return self._xmlrpc.wiki.getRPCVersionSupported()

    @checkerr
    def page(self, page_id, revision=None):
        """Return the raw Wiki text of a given Wiki page.

        Optionally return the information of a Wiki page version (see
        page_versions())

        """
        if not revision:
            return self._xmlrpc.wiki.getPage(page_id)
        else:
            return self._xmlrpc.wiki.getPageVersion(page_id, revision)

    @checkerr
    def page_versions(self, page_id, offset=0):
        """Return a list of available versions for a Wiki page."""
        return self._xmlrpc.wiki.getPageVersions(page_id, offset)

    @checkerr
    def page_info(self, page_id, revision=None):
        """Return information about a given Wiki page.

        Optionally return the information of a Wiki page version (see
        page_versions())

        """
        if not revision:
            return self._xmlrpc.wiki.getPageInfo(page_id)
        else:
            return self._xmlrpc.wiki.getPageInfoVersion(page_id, revision)

    @checkerr
    def page_html(self, page_id, revision=None):
        """Return the (X)HTML body of a Wiki page.

        Optionally return the (X)HTML body of a given Wiki page version (see
        page_versions())

        """
        if not revision:
            return self._xmlrpc.wiki.getPageHTML(page_id)
        else:
            return self._xmlrpc.wiki.getPageHTMLVersion(page_id, revision)

    @checkerr
    def put_page(self, page_id, text, summary='', minor=False):
        """Send a Wiki page to the remote Wiki.

        Keyword arguments:
        page_id -- valpage_id Wiki page page_id
        text -- raw Wiki text (UTF-8 encoded)
        sum -- summary
        minor -- mark as minor edit

        """
        params = {}
        params['sum'] = summary
        params['minor'] = minor
        self._xmlrpc.wiki.putPage(page_id, text, params)

    @checkerr
    def append_page(self, page_id, text, summary='', minor=False):
        """Append text to a Wiki page on the remote Wiki.

        Keyword arguments:
        page_id -- valpage_id Wiki page page_id
        text -- raw Wiki text to append (UTF-8 encoded)
        sum -- summary
        minor -- mark as minor edit

        """
        params = {}
        params['sum'] = summary
        params['minor'] = minor
        self._xmlrpc.dokuwiki.appendPage(page_id, text, params)

    @checkerr
    def pagelist(self, namespace, opts = {'depth': 0, 'hash': False, 'skipacl': False}):
        """Lists all pages within a given namespace.
        
        :param str namespace: The namespace to list pages for
        :param dict opts: Options (optional)
        * :depth: recursion level, default to 0, for all
        * :hash: if True, do the md5 sum of the content, defaults to False
        * :skipacl: if True, list everything regardless of ACL, defaults to False
        """
        return self._xmlrpc.dokuwiki.getPagelist(namespace, opts)

    @checkerr
    def all_pages(self):
        """List all pages of the remote Wiki."""
        return self._xmlrpc.wiki.getAllPages()

    @checkerr
    def backlinks(self, page_id):
        """Return a list of pages that link back to a Wiki page."""
        return self._xmlrpc.wiki.getBackLinks(page_id)

    @checkerr
    def links(self, page_id):
        """Return a list of links contained in a Wiki page."""
        return self._xmlrpc.wiki.listLinks(page_id)

    @checkerr
    def recent_changes(self, timestamp):
        """Return the recent changes since a given timestampe (UTC)."""
        return self._xmlrpc.wiki.getRecentChanges(timestamp)

    @checkerr
    def acl_check(self, page_id):
        """Return the permissions of a Wiki page."""
        return self._xmlrpc.wiki.aclCheck(page_id)

    @checkerr
    def get_file(self, file_id):
        """Download a file from a remote Wiki."""
        # wrap/unwrap data into a binary object instead of base64-encoding/decoding it
        # https://bugs.dokuwiki.org/index.php?do=details&task_id=2662#comment5199
        # and http://docs.python.org/2/library/xmlrpclib.html#binary-objects
        return self._xmlrpc.wiki.getAttachment(file_id).data

    @checkerr
    def put_file(self, file_id, data, overwrite=False):
        """Upload a file to a remote Wiki."""
        # wrap/unwrap data into a binary object instead of base64-encoding/decoding it
        # https://bugs.dokuwiki.org/index.php?do=details&task_id=2662#comment5199
        # and http://docs.python.org/2/library/xmlrpclib.html#binary-objects
        return self._xmlrpc.wiki.putAttachment(file_id, xmlrpclib.Binary(data),
                                               {'ow': overwrite})

    @checkerr
    def delete_file(self, file_id):
        """Delete a file from a remote wiki."""
        return self._xmlrpc.wiki.deleteAttachment(file_id)

    @checkerr
    def file_info(self, file_id):
        """Return information about a given file."""
        return self._xmlrpc.wiki.getAttachmentInfo(file_id)

    @checkerr
    def list_files(self, namespace, recursive=False, pattern=None):
        """List files in a Wiki namespace."""
        options = {}
        if recursive:
            options['recursive'] = True
        if pattern:
            options['pattern'] = pattern
        return self._xmlrpc.wiki.getAttachments(namespace, options)

    @checkerr
    def set_locks(self, locks):
        """
        Lock/unlock a set of files. Locks must be a dictionary which contains
        list of ids to lock/unlock:

            locks =  { 'lock' : [], 'unlock' : [] }
        """
        return self._xmlrpc.dokuwiki.setLocks(locks)

    @checkerr
    def struct_getdata(self, page_id, schema = '',timestamp=0):
        """Get the structured data of a given page."""
        return self._xmlrpc.plugin.struct.getData(page_id, schema, timestamp)

    @checkerr
    def struct_savedata(self, page_id, params={}, summary=''):
        """Saves data for a given page (creates a new revision)."""
        return self._xmlrpc.plugin.struct.saveData(page_id, params, summary)

    @checkerr
    def struct_getschema(self, schema=''):
        """Get the structured data of a given page."""
        return self._xmlrpc.plugin.struct.getSchema(schema)

    @checkerr
    def struct_getaggregationdata(self, schema_names={}, columns={}, aggregation_logic={}, column=''):
        """Get the data that would be shown in an aggregation"""
        return self._xmlrpc.plugin.struct.getAggregationData(schema_names, columns, aggregation_logic, column)


class Callback(object):
    """Callback class used by the option parser.

    Instantiates a new DokuWikiClient. It retrieves and outputs the data for
    the specified callback. The callback is specified in the option parser. The
    option destination has to match a DokuWikiClient method.

    """
    def __init__(self, option, opt_str, value, parser):
        """Initalize callback object."""
        if parser.values.user and parser.values.wiki and parser.values.passwd:
            try:
                self.dokuwiki = DokuWikiClient(parser.values.wiki,
                                               parser.values.user,
                                               parser.values.passwd,
                                               parser.values.http_basic_auth)

                self._parser = parser
                (data, output_format) = self.dispatch(option.dest, value)
            except DokuWikiError as error:
                parser.error(str(error))

            if data:
                if output_format == 'plain':
                    print(data)

                elif output_format == 'list':
                    for item in data:
                        print(item)

                elif output_format == 'dict':
                    if isinstance(data, list):
                        for item in data:
                            for key in item.keys():
                                print('%s: %s' % (key, item[key]))
                            print("\n")
                    else:
                        for key in data.keys():
                            print('%s: %s' % (key, data[key]))

        else:
            parser.print_usage()

    def _get_page_id(self):
        """Check if the additional arguments contain a Wiki page id."""
        try:
            return self._parser.rargs.pop()
        except IndexError:
            self._parser.error('You have to specify a Wiki page.')

    def dispatch(self, option, value):
        """Dispatch the provided callback."""

        callback = self.dokuwiki.__getattribute__(option)

        if option == 'page' or option == 'page_html':
            page_id = self._get_page_id()

            timestamp = self._parser.values.timestamp

            if not timestamp:
                return (callback(page_id), 'plain')
            else:
                return (callback(page_id, timestamp), 'plain')

        elif option == 'append_page':
            page_id = self._get_page_id()
            return (callback(page_id, value), 'dict')

        elif option == 'backlinks':
            page_id = self._get_page_id()
            return (callback(page_id), 'list')

        elif option == 'page_info' or option == 'page_versions' or option == 'links':
            page_id = self._get_page_id()
            return (callback(page_id), 'dict')

        elif option == 'all_pages':
            return (callback(), 'list')

        elif option == 'recent_changes':
            from time import time
            timestamp = self._parser.values.timestamp
            if not timestamp:
                timestamp = int(time())
            return (callback(timestamp), 'dict')


def main():
    """Main function. Invoked when called as script.

    The module can also be used as simple command line client to query a remote
    Wiki. It provides all methods supported by DokuWikis XML-RPC interface. The
    retrieved data is slightly formatted when output.

    """
    from optparse import OptionParser

    parser = OptionParser(version='%prog ' + __version__)

    parser.set_usage('%prog -u <username> -w <wikiurl> -p <passwd> [options] [wiki:page]')

    parser.add_option('-u', '--user',
                      dest='user',
                      help='Username to use when authenticating at the remote Wiki.')

    parser.add_option('-w', '--wiki',
                      dest='wiki',
                      help='The remote wiki.')

    parser.add_option('-p', '--passwd',
                      dest='passwd',
                      help='The user password.')

    parser.add_option('--raw',
                      dest='page',
                      action='callback',
                      callback=Callback,
                      help='Return the raw Wiki text of a Wiki page.')

    parser.add_option('--html',
                      dest='page_html',
                      action='callback',
                      callback=Callback,
                      help='Return the HTML body of a Wiki page.')

    parser.add_option('--info',
                      dest='page_info',
                      action='callback',
                      callback=Callback,
                      help='Return some information about a Wiki page.')

    parser.add_option('--changes',
                      dest='recent_changes',
                      action='callback',
                      callback=Callback,
                      help='List recent changes of the Wiki since timestamp.')

    parser.add_option('--revisions',
                      dest='page_versions',
                      action='callback',
                      callback=Callback,
                      help='Liste page revisions since timestamp.')

    parser.add_option('--backlinks',
                      dest='backlinks',
                      action='callback',
                      callback=Callback,
                      help='Return a list of pages that link back to a Wiki page.')

    parser.add_option('--allpages',
                      dest='all_pages',
                      action='callback',
                      callback=Callback,
                      help='List all pages in the remote Wiki.')

    parser.add_option('--links',
                      dest='links',
                      action='callback',
                      callback=Callback,
                      help='Return a list of links contained in a Wiki page.')

    parser.add_option('--time',
                      dest='timestamp',
                      type='int',
                      help='Revision timestamp.')

    parser.add_option('--http-basic-auth',
                      dest='http_basic_auth',
                      action='store_true',
                      help='Use HTTP Basic Authentication.',
                      default=False)

    parser.add_option('--append',
                      dest='append_page',
                      action='callback',
                      callback=Callback,
                      type='string',
                      help='Append the given text to the wiki page.')

    parser.parse_args()


if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:tw=79:et:
