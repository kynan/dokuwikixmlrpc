#!/usr/bin/env python
# -*- coding: UTF-8 -*-

###############################################################################
# Copyright 2008 by Michael Klier <chi@chimeric.de>
#
# dokuwikixmlrpc - xmlrpc python module to interact with DokuWiki installations
#
# dokuwikixmlrpc free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 only, as published by
# the Free Software Foundation.
#
# dokuwikixmlrpc distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License version 3 for more
# details (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU General Public License version 3
# along with dokuwikixmlrpc. If not, see <http://www.gnu.org/licenses/gpl-2.0.html>
# for a copy of the GPLv2 License.
###############################################################################

# TODO
# allow to overwrite useragent?

"""DokuWiki XMLRPC module.

This modules allows to interact with the XML-RPC interface of DokuWiki
instances. It supports all methods of the DokuWiki XML-RPC interface.
"""

__version__ = '2010-07-19'
__author__  = 'Michael Klier <chi@chimeric.de>'


import xmlrpclib
import base64
from urllib import urlencode
from urllib2 import urlopen
from urllib2 import HTTPError


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


class DokuWikiClient(object):
    """DokuWiki XML-RPC client.

    This class implements a client for DokuWikis XML-RPC interface. All methods
    return exactly the data returned by DokuWikis XML-RPC interface. If
    something goes wrong a method raises a DokuWikiXMLRPCError which contains
    information reported by the XML-RCP interface.
                
    """

    def __init__(self, url, user, passwd, http_basic_auth=False):
        """Initalize everything.

        Try to get a XML-RPC object. If this step fails a DokuWIKIXMLRPCError
        is raised. If the supplied URL is not reachable we raise a
        DokuWikiURLError. Use these to catch bad user input.

        """

        self._url = url
        self._user = user
        self._passwd = passwd
        self._http_basic_auth = http_basic_auth
        self._user_agent = ' '.join([ 'DokuWikiXMLRPC ', 
                                      __version__,
                                      'by (www.chimeric.de)' ])

        self._xmlrpc = self._xmlrpc_init()

        try:
            self.dokuwiki_version = self._dokuwiki_version()
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def _xmlrpc_init(self):
        """Initialize the XMLRPC object."""
        try:
            urlopen(self._url + '/lib/exe/xmlrpc.php?')
        except ValueError:
            raise DokuWikiURLError(self._url)
        except HTTPError:
            raise DokuWikiURLError(self._url)
        
        script = '/lib/exe/xmlrpc.php'

        if not self._http_basic_auth:
            url = ''.join([ self._url, script, '?',
                         urlencode({'u': self._user, 'p':self._passwd}) ])
        else:
            proto, url = self._url.split('://')
            url = proto + '://' + self._user + ':' + self._passwd + '@' + url

        xmlrpclib.Transport.user_agent = self._user_agent
        xmlrpclib.SafeTransport.user_agent = self._user_agent

        return xmlrpclib.ServerProxy(url)


    def _dokuwiki_version(self):
        """Return the DokuWiki version reported by the remote Wiki."""
        try:
            return self._xmlrpc.dokuwiki.getVersion()
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def rpc_version_supported(self):
        """Return the supported RPC version reported by the remote Wiki."""
        try:
            return self._xmlrpc.wiki.getRPCVersionSupported()
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def page(self, page_id, revision=None):
        """Return the raw Wiki text of a given Wiki page.

        Optionally return the information of a Wiki page version (see
        page_versions())
        
        """
        try:
            if not revision:
                return self._xmlrpc.wiki.getPage(page_id)
            else:
                return self._xmlrpc.wiki.getPageVersion(page_id, revision)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def page_versions(self, page_id, offset=0):
        """Return a list of available versions for a Wiki page."""
        try:
            return self._xmlrpc.wiki.getPageVersions(page_id, offset)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def page_info(self, page_id, revision=None):
        """Return information about a given Wiki page.

        Optionally return the information of a Wiki page version (see
        page_versions())
        
        """
        try:
            if not revision:
                return self._xmlrpc.wiki.getPageInfo(page_id)
            else:
                return self._xmlrpc.wiki.getPageInfoVersion(page_id, revision)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def page_html(self, page_id, revision=None):
        """Return the (X)HTML body of a Wiki page.

        Optionally return the (X)HTML body of a given Wiki page version (see
        page_versions())
        
        """
        try:
            if not revision:
                return self._xmlrpc.wiki.getPageHTML(page_id)
            else:
                return self._xmlrpc.wiki.getPageHTMLVersion(page_id, revision)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def put_page(self, page_id, text, summary='', minor=None):
        """Send a Wiki page to the remote Wiki.

        Keyword arguments:
        page_id -- valpage_id Wiki page page_id
        text -- raw Wiki text (UTF-8 encoded)
        sum -- summary
        minor -- mark as minor edit
        
        """
        try:
            params = {}
            params['sum'] = summary
            params['minor'] = minor
            self._xmlrpc.wiki.putPage(page_id, text, params)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def all_pages(self):
        """List all pages of the remote Wiki."""
        try:
            return self._xmlrpc.wiki.getAllPages()
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def backlinks(self, page_id):
        """Return a list of pages that link back to a Wiki page."""
        try:
            return self._xmlrpc.wiki.getBackLinks(page_id)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def links(self, page_id):
        """Return a list of links contained in a Wiki page."""
        try:
            return self._xmlrpc.wiki.listLinks(page_id)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def recent_changes(self, timestamp):
        """Return the recent changes since a given timestampe (UTC)."""
        try:
            return self._xmlrpc.wiki.getRecentChanges(timestamp)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def acl_check(self, page_id):
        """Return the permissions of a Wiki page."""
        try:
            return self._xmlrpc.wiki.aclCheck(page_id)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

    def get_file(self, file_id):
        """Download a file from a remote Wiki."""
        try:
            return base64.b64decode(self._xmlrpc.wiki.getAttachment(file_id))
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

    def put_file(self, file_id, data, overwrite = False):
        """Upload a file to a remote Wiki."""
        try:
            return self._xmlrpc.wiki.putAttachment(file_id, 
                   base64.b64encode(data), {'ow': overwrite})
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

    def delete_file(self, file_id):
        """Delete a file from a remote wiki."""
        try:
            return self._xmlrpc.wiki.deleteAttachment(file_id)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

    def file_info(self, file_id):
        """Return information about a given file."""
        try:
            return self._xmlrpc.wiki.getAttachmentInfo(file_id)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

    def list_files(self, namespace, recursive = False, pattern = None):
        """List files in a Wiki namespace."""
        options = {}
        if recursive:
            options['recursive'] = True
        if pattern:
            options['pattern'] = pattern
        try:
            return self._xmlrpc.wiki.getAttachments(namespace, options)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


    def set_locks(self, locks):
        """
        Lock/unlock a set of files. Locks must be a dictionary which contains
        list of ids to lock/unlock:

            locks =  { 'lock' : [], 'unlock' : [] }
        """
        try:
            return self._xmlrpc.dokuwiki.setLocks(locks)
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)


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
            except DokuWikiXMLRPCError, error:
                parser.error(error)

            except DokuWikiURLError, error:
                parser.error(error)

            self._parser = parser
            (data, output_format) = self.dispatch(option.dest)

            if data:
                if output_format == 'plain':
                    print data

                elif output_format == 'list':
                    for item in data:
                        print item

                elif output_format == 'dict':
                    if type(data) == type([]):
                        for item in data:
                            for key in item.keys():
                                print '%s: %s' % (key, item[key])
                            print "\n"
                    else:
                        for key in data.keys():
                            print '%s: %s' % (key, data[key])


        else:
            parser.print_usage()


    def _get_page_id(self):
        """Check if the additional arguments contain a Wiki page id."""
        try:
            return self._parser.rargs.pop()
        except IndexError:
            self._parser.error('You have to specify a Wiki page.')


    def dispatch(self, option):
        """Dispatch the provided callback."""

        callback = self.dokuwiki.__getattribute__(option)

        if option == 'page' or option == 'page_html':
            page_id = self._get_page_id()

            timestamp = self._parser.values.timestamp

            if not timestamp:
                return (callback(page_id), 'plain')
            else:
                return (callback(page_id, timestamp), 'plain')

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
    
    parser = OptionParser(version = '%prog ' + __version__)

    parser.set_usage('%prog -u <username> -w <wikiurl> -p <passwd> [options] [wiki:page]')

    parser.add_option('-u', '--user', 
            dest = 'user', 
            help = 'Username to use when authenticating at the remote Wiki.')

    parser.add_option('-w', '--wiki',
            dest = 'wiki',
            help = 'The remote wiki.')

    parser.add_option('-p', '--passwd',
            dest = 'passwd',
            help = 'The user password.')

    parser.add_option('--raw',
            dest = 'page',
            action = 'callback',
            callback = Callback,
            help = 'Return the raw Wiki text of a Wiki page.')

    parser.add_option('--html',
            dest = 'page_html',
            action = 'callback',
            callback = Callback,
            help = 'Return the HTML body of a Wiki page.')

    parser.add_option('--info',
            dest = 'page_info',
            action = 'callback',
            callback = Callback,
            help = 'Return some information about a Wiki page.')

    parser.add_option('--changes',
            dest = 'recent_changes',
            action = 'callback',
            callback = Callback,
            help = 'List recent changes of the Wiki since timestamp.')

    parser.add_option('--revisions',
            dest = 'page_versions',
            action = 'callback',
            callback = Callback,
            help = 'Liste page revisions since timestamp.')

    parser.add_option('--backlinks',
            dest = 'backlinks',
            action = 'callback',
            callback = Callback,
            help = 'Return a list of pages that link back to a Wiki page.')

    parser.add_option('--allpages',
            dest = 'all_pages',
            action = 'callback',
            callback = Callback,
            help = 'List all pages in the remote Wiki.')

    parser.add_option('--links',
            dest = 'links',
            action = 'callback',
            callback = Callback,
            help = 'Return a list of links contained in a Wiki page.')

    parser.add_option('--time',
            dest = 'timestamp',
            type = 'int',
            help = 'Revision timestamp.')
    
    parser.add_option('--http-basic-auth',
            dest = 'http_basic_auth',
            action = 'store_true',
            help = 'Use HTTP Basic Authentication.',
            default=False)

    parser.parse_args()


if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:tw=79:et:enc=utf-8:
