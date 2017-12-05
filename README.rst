fpyutils
========

A collection of useful non-standard Python functions which aim to be simple to
use, highly readable but not efficient.


An example:

    >>> from fpyutils import filelines
    >>> f = open('foo.txt')
    >>> f.read()
    "This is\nfoo.\nfoo\nThis is\nnot\nbar.\nAnd it's\n    foo\n\nBye!\n"
    >>> import fpyutils
    >>> fpyutils.get_line_matches('foo.txt','foo',5)
    {1: 3, 2: 8}

Documentation
-------------

http://frnmst.github.io/fpyutils

Conventions
-----------

- PEP.
- For each module ``m.py`` it exists, if necessary, its utility file called ``_m.py``
- 4 space indentation.

Workflow for implementing new modules
-------------------------------------

1. Define your idea
2. Implement a unit test class
3. Write the code
4. Test it (run ``make test``)
5. PEP standards compliancy (run ``make pep``)
6. Update the documentation (run ``make doc``)
7. Make a pull request

License
-------

Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
<franco.masotti@student.unife.it>

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
