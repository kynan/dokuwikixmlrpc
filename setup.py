from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="dokuwikixmlrpc",
    version="2022.12.22",
    description="DokuWiki XML-RPC module.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    py_modules=["dokuwikixmlrpc"],
    author="Michael Klier",
    author_email="chi@chimeric.de",
    maintainer="Florian Rathgeber",
    maintainer_email="florian.rathgeber@gmail.com",
    url="https://github.com/kynan/dokuwikixmlrpc",
    download_url="https://github.com/downloads/kynan/dokuwikixmlrpc/dokuwikixmlrpc.tgz",
    keyword=["dokuwiki", "xmlrpc", "xml-rpc"],
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
# vim:ts=4:sw=4:et:
