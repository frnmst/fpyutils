# -*- coding: utf-8 -*-
#
# filelines.py
#
# Copyright (C) 2017-2023 Franco Masotti (see /README.md)
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
from __future__ import annotations

import os
import shutil
import sys
import tempfile

from .exceptions import LineOutOfFileBoundsError, NegativeLineRangeError


def get_line_matches(
        input_file: str,
        pattern: str,
        max_occurrencies: int = 0,
        loose_matching: bool = True,
        keep_all_lines: bool = False) -> tuple[dict[int, int], str]:
    r"""Get the line numbers of matched patterns and the matched string itself.

    :parameter input_file: the file that needs to be read.
    :parameter pattern: the pattern that needs to be searched.
    :parameter max_occurrencies: the maximum number of expected occurrencies.
         Defaults to ``0`` which means that all occurrencies will be matched.
         This parameter is limited by the platform (``sys.maxsize``).
    :parameter loose_matching: ignore leading and trailing whitespace
         characters for both pattern and matched strings. Defaults to ``True``.
    :parameter keep_all_lines: if set to ``True`` returns the whole file content
         as a string. Defaults to ``False``.
    :type input_file: str
    :type pattern: str
    :type max_occurrencies: int
    :type loose_matching: bool
    :type keep_all_lines: bool
    :returns: occurrency_matches, a dictionary where each key corresponds
         to the number of occurrencies and each value to the matched line number.
         If no match was found for that particular occurrency, the key is not
         set. This means means for example: if the first occurrency of
         pattern is at line y then: x[1] = y, with x being the dictionary.

         lines, a string corresponding to the matched lines or the whole file
         (see ``keep_all_lines`` argument).
    :rtype: tuple[dict[int, int], str]
    :raises: a built-in exception.

    .. note::
         Line numbers start from ``1``.
    """
    if max_occurrencies < 0 or max_occurrencies > sys.maxsize:
        raise ValueError

    occurrency_counter: int = 0
    occurrency_matches: dict[int, int] = dict()
    lines: list[str] = list()
    line_original: str

    if max_occurrencies == 0:
        # See
        # https://docs.python.org/3/whatsnew/3.0.html#integers
        max_occurrencies = sys.maxsize
    if loose_matching:
        pattern = pattern.strip()

    line_counter: int = 1
    with open(input_file, 'r') as f:
        line = f.readline()
        while line and (keep_all_lines
                        or occurrency_counter < max_occurrencies):
            line_original = line
            if loose_matching:
                line = line.strip()

            if line == pattern and occurrency_counter < max_occurrencies:
                occurrency_counter += 1
                occurrency_matches[occurrency_counter] = line_counter
                lines.append(line_original)
            elif keep_all_lines:
                lines.append(line_original)

            line = f.readline()
            line_counter += 1

    return occurrency_matches, ''.join(lines)


def insert_string_at_line(input_file: str,
                          string_to_be_inserted: str,
                          put_at_line_number: int,
                          output_file: str,
                          append: bool = True,
                          newline_character: str = os.linesep):
    r"""Write a string at the specified line.

    :parameter input_file: the file that needs to be read.
    :parameter string_to_be_inserted: the string that needs to be added.
    :parameter put_at_line_number: the line number on which to append the
         string.
    :parameter output_file: the file that needs to be written with the new
         content.
    :parameter append: decides whether to append or prepend the string at the
         selected line. Defaults to ``True``.
    :parameter newline_character: set the character used to fill the file
         in case line_number is greater than the number of lines of
         input_file. Defaults to the default platform newline,
         i.e: ``os.linesep``.
    :type input_file: str
    :type string_to_be_inserted: str
    :type line_number: int
    :type output_file: str
    :type append: bool
    :type newline_character: str
    :returns: None
    :raises: a built-in exception.

    .. note::
         Line numbers start from ``1``.

    .. note::
         Existing line endings of the input file are changed to
         ``newline_character``.
    """
    if put_at_line_number < 1:
        raise ValueError

    line_counter: int = 1
    loop: bool = True
    subst_done: bool = False
    final_string: list[str] = list()
    with open(input_file, 'r') as f:
        while loop:
            current_line: str = f.readline()
            while current_line:
                # Lines match.
                if line_counter == put_at_line_number:
                    subst_done = True
                    if append:
                        # Append.
                        final_string.append(current_line)
                        final_string.append(string_to_be_inserted)
                    else:
                        # Prepend.
                        final_string.append(string_to_be_inserted)
                        final_string.append(current_line)
                else:
                    # No match, generic line.
                    final_string.append(current_line)
                current_line = f.readline()
                line_counter += 1
            while not current_line and line_counter <= put_at_line_number:
                # Out of file bounds.
                if line_counter == put_at_line_number:
                    final_string.append(string_to_be_inserted)
                    line_counter += 1
                    # Prepend does not make sense here since we are out of the
                    # file bounds so the `string_to_be_inserted` will always
                    # be the last string inserted in the file.
                else:
                    final_string.append(newline_character)
                    line_counter += 1

            if not current_line or (line_counter > put_at_line_number
                                    and subst_done):
                # All the file has been iterated by this point and the
                # substitution has been done either in or out of the file
                # bounds.
                loop = False

    # Atomic write.
    # See
    # https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
    # https://docs.python.org/3/library/os.html#os.fsync
    with tempfile.NamedTemporaryFile('w',
                                     newline=newline_character,
                                     delete=False) as f:
        f.flush()
        os.fsync(f.fileno())
        f.write(''.join(final_string))
    shutil.move(f.name, output_file)


def remove_line_interval(input_file: str, delete_line_from: int,
                         delete_line_to: int, output_file: str):
    r"""Remove a line interval.

    :parameter input_file: the file that needs to be read.
    :parameter delete_line_from: the line number from which start deleting.
    :parameter delete_line_to: the line number to which stop deleting.
    :parameter output_file: the file that needs to be written without the
         selected lines.
    :type input_file: str
    :type delete_line_from: int
    :type delete_line_to: int
    :type output_file: str
    :returns: None
    :raises: NegativeLineRangeError, LineOutOfFileBoundsError
         or a built-in exception.

    .. note::
         Line numbers start from ``1``.

    .. note::
         It is possible to remove a single line only. This happens when
         the parameters delete_line_from and delete_line_to are equal.
    """
    # Invalid line ranges.
    if delete_line_from < 1 or delete_line_to < 1:
        raise ValueError
    # Base case delete_line_to - delete_line_from == 0: single line.
    if delete_line_to - delete_line_from < 0:
        raise NegativeLineRangeError

    line_counter: int = 1
    line_to_write: list[str] = list()
    line: str

    # Rewrite the file without the string.
    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            # Ignore the line interval where the content to be deleted lies.
            if line_counter >= delete_line_from and line_counter <= delete_line_to:
                pass
            # Write the rest of the file.
            else:
                line_to_write.append(line)
            line_counter += 1
            line = f.readline()

    # Invalid line range.
    if delete_line_from > line_counter or delete_line_to > line_counter:
        raise LineOutOfFileBoundsError

    # Atomic write.
    # See
    # https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
    # https://docs.python.org/3/library/os.html#os.fsync
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.flush()
        os.fsync(f.fileno())
        f.write(''.join(line_to_write))
    shutil.move(f.name, output_file)


if __name__ == '__main__':
    pass
