.. image:: https://img.shields.io/pypi/dm/dokuwikixmlrpc
    :target: https://pypi.org/project/dokuwikixmlrpc
.. image:: https://img.shields.io/pypi/v/dokuwikixmlrpc
    :target: https://pypi.org/project/dokuwikixmlrpc
.. image:: https://img.shields.io/pypi/pyversions/dokuwikixmlrpc
    :target: https://pypi.org/project/dokuwikixmlrpc
.. image:: https://img.shields.io/pypi/format/dokuwikixmlrpc
    :target: https://pypi.org/project/dokuwikixmlrpc
.. image:: https://img.shields.io/pypi/l/dokuwikixmlrpc
    :target: https://raw.githubusercontent.com/kynan/dokuwikixmlrpc/master/LICENSE.txt
.. image:: https://img.shields.io/github/stars/kynan/dokuwikixmlrpc?style=social
    :target: https://github.com/kynan/dokuwikixmlrpc/stargazers
.. image:: https://img.shields.io/github/forks/kynan/dokuwikixmlrpc?style=social
    :target: https://github.com/kynan/dokuwikixmlrpc/network/member

``dokuwikixmlrpc`` is a python module which implements `DokuWiki's XML-RPC
interface <https://www.dokuwiki.org/devel:xmlrpc>`_.

Installation: ::

    pip install dokuwikixmlrpc

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