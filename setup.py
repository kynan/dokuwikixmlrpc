# dokuwikixmlrpc's setup.py

# Try importing setup from setuptools to get e.g. the develop command
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "dokuwikixmlrpc",
    version = "2010-07-19",
    description = "DokuWiki XML-RPC module.",
    py_modules = ["dokuwikixmlrpc"],
    author = "Michael Klier",
    author_email = "chi@chimeric.de",
    url = "http://github.com/chimeric/dokuwikixmlrpc",
    download_url = "http://github.com/downloads/chimeric/dokuwikixmlrpc/dokuwikixmlrpc.tgz",
    keyword = ["xmlrpc", "dokuwiki"],
    classfiers = [
        "Programming Language :: Python",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
)
# vim:ts=4:sw=4:et:
