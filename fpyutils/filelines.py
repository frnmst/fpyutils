#
# filelines.py
#
# Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
#
# This file is part of fpyutils.
#
# fpyutils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fpyutils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fpyutils.  If not, see <http://www.gnu.org/licenses/>.
#
"""Functions on reading and writing files by line."""

from .exceptions import (LineOutOfFileBoundsError)


def get_line_matches(input_file,
                     pattern,
                     max_occurrencies,
                     loose_matching=True):
    r"""Get the line numbers of matched patterns.

    :parameter input_file: the file that needs to be read.
    :parameter pattern: the pattern that needs to be searched.
    :parameter max_occurrencies: the maximum number of expected occurrencies.
    :parameter loose_matching: ignore leading and trailing whitespace
      characters for both pattern and matched strings. Defaults to ``True``.
    :type input_file: str
    :type pattern: str
    :type max_occurrencies: int or float
    :type loose_matching: bool
    :returns: A dictionary where each key corresponds to the number of
      occurrency and each value to the matched line number.
      If no match was found for that particular occurrency, the key is not
      set.
    :rtype: dict
    :raises: LineOutOfFileBoundsError or the built-in exceptions.

    .. warning:: The parameter max_occurrencies must be greater than
        zero.

    .. note:: To get all occurrencies of a pattern, the parameter
        max_occurrencies must be set to ``float('inf')``.

    :Example:

    >>> f = open('foo.txt')
    >>> f.read()
    "This is\nfoo.\nfoo\nThis is\nnot\nbar.\nAnd it's\n    foo\n\nBye!\n"
    >>> import fpyutils
    >>> fpyutils.get_line_matches('foo.txt','foo',5)
    {1: 3, 2: 8}
    """
    assert isinstance(input_file, str)
    assert isinstance(pattern, str)
    assert (isinstance(max_occurrencies, int) or
            isinstance(max_occurrencies, float))
    assert max_occurrencies > 0

    occurrency_counter = 0
    occurrency_matches = dict()

    # 1. Strip all whitespaces from pattern if requested.
    if loose_matching:
        pattern = pattern.strip()

    line_number = 1
    with open(input_file, 'r') as f:
        # 2. Read the first line.
        line = f.readline()
        while (line and float(occurrency_counter) < float(max_occurrencies)):
            # 3.1. Strip all whitespaces from line if requested.
            if loose_matching:
                line = line.strip()
            # 3.2. Check if line corresponds to the pattern.
            if line == pattern:
                occurrency_counter += 1
                occurrency_matches[occurrency_counter] = line_number
            # 3.3. Go to the next line.
            line = f.readline()
            line_number += 1

    return occurrency_matches


def insert_string_at_line(input_file, string_to_be_inserted, line_number,
                          output_file):
    r"""Write a string at the specified line.

    :parameter input_file: the file that needs to be read.
    :parameter string_to_be_inserted: the string that needs to be added.
    :parameter line_number: the line number on which to append the string.
    :parameter output_file: the file that needs to be written with the new
      content.
    :type input_file: str
    :type string_to_be_inserted: str
    :type line_number: int
    :type output_file: str
    :returns: None
    :raises: LineOutOfFileBoundsError or the built-in exceptions.

    .. warning:: The parameter line_number must be greater than
        zero.

    .. note:: string_to_be_inserted will be appended to the selected line.

    :Example:

    >>> f = open('foo.txt', r)
    >>> f.read()
    'This is\nfoo.\nThis is\nnot\nbar.\n\nBye!\n'
    >>> import fpyutils
    >>> fpyutils.insert_string_at_line('foo.txt','bar',2,'bar.txt')
    >>> f = open('bar.txt')
    >>> f.read()
    'This is\nfoo.\nbarThis is\nnot\nbar.\n\nBye!\n'
    """
    assert isinstance(input_file, str)
    assert isinstance(string_to_be_inserted, str)
    assert isinstance(line_number, int)
    assert isinstance(output_file, str)
    assert line_number > 0

    # 1. Read the whole file.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 2. Raise an exception if we are trying to write on a non-existing line.
    if line_number > len(lines):
        raise LineOutOfFileBoundsError

    line_counter = 1
    # 3. Rewrite the file with the toc.
    with open(output_file, 'w') as f:
        for line in lines:
            if line_counter == line_number:
                # A very simple append operation: if the original line ends
                # with a '\n' character, the toc will be added on the next
                # line.
                line += string_to_be_inserted
            f.write(line)
            line_counter += 1


def remove_line_interval(input_file, line_from, line_to, output_file):
    r"""Remove a line interval.

    :parameter input_file: the file that needs to be read.
    :parameter line_from: the line number from which start deleting.
    :parameter line_to: the line number to which stop deleting.
    :parameter output_file: the file that needs to be written without the
      selected lines.
    :type input_file: str
    :type line_from: int
    :type line_to: int
    :type output_file: str
    :returns: None
    :raises: LineOutOfFileBoundsError or the built-in exceptions.

    .. warning:: The parameters line_from and line_to must be greater than
        zero.

    .. note:: It is possible to remove a single line only. This happens when
        the parameters line_from and line_to are equal.

    :Example:

    >>> f = open('foo.txt', r)
    >>> f.read()
    'This is\nfoo.\nThis is\nnot\nbar.\n\nBye!\n'
    >>> import fpyutils
    >>> fpyutils.insert_string_at_line('foo.txt','bar',2,'bar.txt')
    >>> f = open('bar.txt')
    >>> f.read()
    'This is\nfoo.\nbarThis is\nnot\nbar.\n\nBye!\n'
    """
    assert isinstance(input_file, str)
    assert isinstance(line_from, int)
    assert isinstance(output_file, str)
    assert isinstance(line_to, int)
    # At least one line must be deleted.
    # Base case line_to - line_from == 0, corresponds to a single line.
    assert line_to - line_from >= 0
    assert line_from > 0
    assert line_to > 0

    # 1. Read the whole file.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 2. Save the total lines.
    total_lines = len(lines)

    # 3. Raise an exception if we are trying to delete an invalid line.
    if (line_from > total_lines or line_to > total_lines):
        raise LineOutOfFileBoundsError

    line_number = 1
    # 3. Rewrite the file without the toc.
    with open(output_file, 'w') as f:
        for line in lines:
            # Ignore the line interval where the content to be deleted lies.
            if line_number >= line_from and line_number <= line_to:
                pass
            # Write the rest of the file.
            else:
                f.write(line)
            line_number += 1


if __name__ == '__main__':
    pass
