fpyutils
========

|pypiver|    |license|    |pyver|    |downloads|    |dependentrepos|    |buymeacoffee|

.. |pypiver| image:: https://img.shields.io/pypi/v/fpyutils.svg
               :alt: PyPI fpyutils version

.. |license| image:: https://img.shields.io/pypi/l/fpyutils.svg?color=blue
               :alt: PyPI - License
               :target: https://raw.githubusercontent.com/frnmst/fpyutils/master/LICENSE.txt

.. |pyver| image:: https://img.shields.io/pypi/pyversions/fpyutils.svg
             :alt: PyPI - Python Version

.. |downloads| image:: https://pepy.tech/badge/fpyutils
                 :alt: Downloads
                 :target: https://pepy.tech/project/fpyutils

.. |dependentrepos| image:: https://img.shields.io/librariesio/dependent-repos/pypi/fpyutils.svg
                      :alt: Dependent repos (via libraries.io)
                      :target: https://libraries.io/pypi/fpyutils/dependents

.. |buymeacoffee| image:: assets/buy_me_a_coffee.svg
                   :alt: Buy me a coffee
                   :target: https://buymeacoff.ee/frnmst

A collection of useful non-standard Python functions which aim to be simple to
use, highly readable but not efficient.

Documentation
-------------

http://frnmst.github.io/fpyutils

API examples
------------


::


    >>> import fpyutils
    >>> f = open('foo.txt')
    >>> f.read()
    "This is\nfoo.\nfoo\nThis is\nnot\nbar.\nAnd it's\n    foo\n\nBye!\n"
    >>> fpyutils.filelines.get_line_matches('foo.txt','foo',5)
    {1: 3, 2: 8}


.. _public API: https://frnmst.github.io/fpyutils/api.html

License
-------

Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>

fpyutils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fpyutils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fpyutils.  If not, see <http://www.gnu.org/licenses/>.

Trusted source
--------------

You can check the authenticity of new releases using my public key.

Instructions, sources and keys can be found at `frnmst.gitlab.io/software <https://frnmst.gitlab.io/software/>`_.
