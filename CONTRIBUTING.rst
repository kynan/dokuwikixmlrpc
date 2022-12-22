How to contribute
=================

Development happens on GitHub_ - `bug reports`_ and `pull requests`_ welcome!

Tagging a new version
---------------------

dokuwikixmlrpc uses date based versioning. To release a version with today's
date, follow these steps. ::

    VERSION=$(date +%Y.%m.%d)

To simplify updating the version number consistently across different files
and creating the appropriate annotated tag, we use bump2version_. For the first
new release in a year, run ::

    bump2version --new-version $VERSION major

and for subsequent releases ::

    bump2version --new-version $VERSION minor

Remember to also push the release tag with ``git push --tags``.

Packaging and releasing on PyPI
-------------------------------

Build the source distribution and wheel using `build`_: ::

    python -m build

Use twine_ to verify and upload the new release to PyPI. ::

    twine check dist/dokuwikixmlrpc-${VERSION}*

Then upload to test PyPI first: ::

    twine upload -r testpypi dist/dokuwikixmlrpc-${VERSION}*

If everything looks sane, upload to the "real" PyPI: ::

    twine upload dist/dokuwikixmlrpc-${VERSION}*

.. _GitHub: https://github.com/kynan/dokuwikixmlrpc
.. _bug reports: https://github.com/kynan/dokuwikixmlrpc/issues
.. _pull requests: https://github.com/kynan/dokuwikixmlrpc/pulls
.. _bump2version: https://github.com/c4urself/bump2version
.. _build: https://pypi.org/project/build/
.. _twine: https://twine.readthedocs.io/en/latest/#using-twine
