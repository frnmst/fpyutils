fpyutils
========

A collection of useful non-standard Python functions which aim to be simple to
use, highly readable but not efficient.


    >>> from fpyutils import filelines
    >>> f = open('foo.txt')
    >>> f.read()
    "This is\nfoo.\nfoo\nThis is\nnot\nbar.\nAnd it's\n    foo\n\nBye!\n"
    >>> import fpyutils
    >>> fpyutils.get_line_matches('foo.txt','foo',5)
    {1: 3, 2: 8}


Conventions
-----------

- PEP.
- For each module ``m.py`` it exists, if necessary, its utility file called ``_m.py``


New modules workflow
--------------------

1. Write your idea
2. Write a unit test class
3. Implement it
4. Test it
5. Check if PEP standards are respected (run ```make pep```)
6. Update the documentation
7. Make a pull request
