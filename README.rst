.. image:: https://img.shields.io/pypi/dm/dokuwikixmlrpc.svg
    :target: https://pypi.org/project/dokuwikixmlrpc
.. image:: https://img.shields.io/pypi/v/dokuwikixmlrpc.svg
    :target: https://pypi.org/project/dokuwikixmlrpc
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/kynan/dokuwikixmlrpc/master/LICENSE.txt
``dokuwikixmlrpc`` is a python module which implements `DokuWiki's XML-RPC
interface <https://www.dokuwiki.org/devel:xmlrpc>`_.

It can be used to send/retrieve data from remote DokuWiki instances: ::

    import dokuwikixmlrpc
    dw = DokuWikiClient('https://mywikiurl.com', 'wikiuser', 'wikipassword')
    print(dw.dokuwiki_version)
    print(dw.pagelist(':'))

The module can be executed as a standalone script (this is mainly for testing
purposes). Call ::

    python -m dokuwikixmlrpc --help

for more information.

Copyright 2009 by Michael Klier <chi@chimeric.de>.

See `LICENSE.txt <LICENSE.txt>`_ for license info.