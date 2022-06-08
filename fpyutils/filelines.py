#
# filelines.py
#
# Copyright (C) 2017-2020 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
import os

import atomicwrites
from atomicwrites import atomic_write

from .exceptions import LineOutOfFileBoundsError, NegativeLineRangeError


def get_line_matches(input_file: str,
                     pattern: str,
                     max_occurrencies: int = 0,
                     loose_matching: bool = True,
                     keep_all_lines: bool = False) -> tuple:
    r"""Get the line numbers of matched patterns and the matched string itself.

    :parameter input_file: the file that needs to be read.
    :parameter pattern: the pattern that needs to be searched.
    :parameter max_occurrencies: the maximum number of expected occurrencies.
         Defaults to ``0`` which means that all occurrencies will be matched.
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
    :rtype: tuple
    :raises: a built-in exception.

    .. note::
         Line numbers start from ``1``.
    """
    if max_occurrencies < 0:
        raise ValueError

    occurrency_counter: float = 0.0
    occurrency_matches: dict = dict()
    lines: list = list()
    line_original: str

    if max_occurrencies == 0:
        max_occurrencies = float('inf')
    if loose_matching:
        pattern = pattern.strip()

    line_counter: int = 1
    with open(input_file, 'r') as f:
        line = f.readline()
        while line and (keep_all_lines or occurrency_counter < max_occurrencies):
            line_original = line
            if loose_matching:
                line = line.strip()

            if line == pattern and occurrency_counter < max_occurrencies:
                occurrency_counter += 1.0
                occurrency_matches[int(occurrency_counter)] = line_counter
                lines.append(line_original)
            elif keep_all_lines:
                lines.append(line_original)

            line = f.readline()
            line_counter += 1

    lines = ''.join(lines)

    return occurrency_matches, lines


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
    :raises: LineOutOfFileBoundsError or a built-in exception.

    .. note::
         Line numbers start from ``1``.

    .. note::
         Exsisting line endings of the input file are changed to
         ``newline_character``.
    """
    if put_at_line_number < 1:
        raise ValueError

    with open(input_file, 'r') as f:
        lines: str = f.readlines()

    line_counter: int = 1
    lines_length: int = len(lines)
    i: int = 0
    loop: bool = True
    extra_lines_done: bool = False
    line_number_after_eof: int = len(lines) + 1

    # Atomicwrites does not support the newline argument so
    # all the file writing is done in binary mode.
    c = atomicwrites.AtomicWriter(output_file, 'w', overwrite=True, newline=newline_character)
    with c.open() as f:
        while loop:

            if put_at_line_number > len(
                    lines) and line_counter == line_number_after_eof:
                # There are extra lines to write.
                line = str()
            else:
                line = lines[i]

            # It is ok if the position of line to be written is greater
            # than the last line number of the input file. We just need to add
            # the appropriate number of newline characters which will fill
            # the non existing lines of the output file.
            if (put_at_line_number > lines_length
               and line_counter == line_number_after_eof):
                for additional_newlines in range(
                        0, put_at_line_number - len(lines) - 1):
                    # Skip the newline in the line where we need to insert
                    # the new string.
                    f.write(newline_character)
                    line_counter += 1
                    i += 1
                extra_lines_done = True

            if line_counter == put_at_line_number:
                # A very simple append operation: if the original line ends
                # with a '\n' character, the string will be added on the next
                # line...
                if append:
                    line = line + string_to_be_inserted
                # ...otherwise the string is prepended.
                else:
                    line = string_to_be_inserted + line
            f.write(line)
            line_counter += 1
            i += 1
            # Quit the loop if there is nothing more to write.
            if i >= lines_length:
                loop = False
            # Continue looping if there are still extra lines to write.
            if put_at_line_number > lines_length and not extra_lines_done:
                loop = True

        # endwhile

    # endwith


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
    :raises: LineOutOfFileBoundsError or a built-in exception.

    .. note::
         Line numbers start from ``1``.

    .. note::
         It is possible to remove a single line only. This happens when
         the parameters delete_line_from and delete_line_to are equal.
    """
    if delete_line_from < 1:
        raise ValueError
    if delete_line_to < 1:
        raise ValueError

    with open(input_file, 'r') as f:
        lines: str = f.readlines()
    lines_length: int = len(lines)

    # Invalid line ranges.
    # Base case delete_line_to - delete_line_from == 0: single line.
    if delete_line_to - delete_line_from < 0:
        raise NegativeLineRangeError
    if delete_line_from > lines_length or delete_line_to > lines_length:
        raise LineOutOfFileBoundsError

    line_counter: int = 1
    # Rewrite the file without the string.
    with atomic_write(output_file, overwrite=True) as f:
        for line in lines:
            # Ignore the line interval where the content to be deleted lies.
            if line_counter >= delete_line_from and line_counter <= delete_line_to:
                pass
            # Write the rest of the file.
            else:
                f.write(line)
            line_counter += 1


if __name__ == '__main__':
    pass
