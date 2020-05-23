# Try importing setup from setuptools to get e.g. the develop command
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = "dokuwikixmlrpc",
    version = "2020.5.23",
    description="DokuWiki XML-RPC module.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    py_modules = ["dokuwikixmlrpc"],
    author = "Michael Klier",
    author_email = "chi@chimeric.de",
    url = "https://github.com/kynan/dokuwikixmlrpc",
    download_url = "https://github.com/downloads/kynan/dokuwikixmlrpc/dokuwikixmlrpc.tgz",
    keyword = ["xmlrpc", "dokuwiki"],
    license="License :: OSI Approved :: MIT License",
    classfiers = [
        "Programming Language :: Python",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
# vim:ts=4:sw=4:et:
