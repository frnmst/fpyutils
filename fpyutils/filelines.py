#
# filelines.py
#
# Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
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


def get_line_matches(input_file: str,
                     pattern: str,
                     max_occurrencies: int = 0,
                     loose_matching: bool = True) -> dict:
    r"""Get the line numbers of matched patterns.

    :parameter input_file: the file that needs to be read.
    :parameter pattern: the pattern that needs to be searched.
    :parameter max_occurrencies: the maximum number of expected occurrencies.
         Defaults to ``0`` which means that all occurrencies will be matched.
    :parameter loose_matching: ignore leading and trailing whitespace
         characters for both pattern and matched strings. Defaults to ``True``.
    :type input_file: str
    :type pattern: str
    :type max_occurrencies: int
    :type loose_matching: bool
    :returns: occurrency_matches, A dictionary where each key corresponds
         to the number of occurrencies and each value to the matched line number.
         If no match was found for that particular occurrency, the key is not
         set. This means means for example: if the first occurrency of
         pattern is at line y then: x[1] = y.
    :rtype: dict
    :raises: a built-in exception.
    """
    assert max_occurrencies >= 0

    occurrency_counter = 0.0
    occurrency_matches = dict()

    if max_occurrencies == 0:
        max_occurrencies = float('inf')
    if loose_matching:
        pattern = pattern.strip()

    put_at_line_number = 1
    with open(input_file, 'r') as f:
        line = f.readline()
        while line and occurrency_counter < max_occurrencies:
            if loose_matching:
                line = line.strip()
            if line == pattern:
                occurrency_counter += 1.0
                occurrency_matches[int(
                    occurrency_counter)] = put_at_line_number
            line = f.readline()
            put_at_line_number += 1

    return occurrency_matches


def insert_string_at_line(input_file: str,
                          string_to_be_inserted: str,
                          put_at_line_number: int,
                          output_file: str,
                          append: bool = True,
                          newline_character: str = '\n'):
    r"""Write a string at the specified line.

    :parameter input_file: the file that needs to be read.
    :parameter string_to_be_inserted: the string that needs to be added.
    :parameter line_number: the line number on which to append the string.
    :parameter output_file: the file that needs to be written with the new
         content.
    :parameter append: decides whether to append or prepend the string at the
         selected line. Defaults to ``True``.
    :parameter newline_character: set the character used to fill the file
         in case line_number is greater than the number of lines of
         input_file. Defaults to ``\n``.
    :type input_file: str
    :type string_to_be_inserted: str
    :type line_number: int
    :type output_file: str
    :type append: bool
    :type newline_character: str
    :returns: None
    :raises: LineOutOfFileBoundsError or a built-in exception.
    """
    assert put_at_line_number >= 1

    with open(input_file, 'r') as f:
        lines = f.readlines()

    line_counter = 1
    i = 0
    loop = True
    extra_lines_done = False
    with open(output_file, 'w') as f:
        while loop:
            line_number_after_eof = len(lines) + 1
            if put_at_line_number > len(
                    lines) and line_counter == line_number_after_eof:
                # There are extra lines to write.
                line = str()
            else:
                line = lines[i]
            # It is ok if the position of line to be written is greater
            # than the last line number of the input file. We just need to add
            # the appropriate number of new line characters which will fill
            # the non existing lines of the output file.
            if put_at_line_number > len(
                    lines) and line_counter == line_number_after_eof:
                for x in range(0, put_at_line_number - len(lines)):
                    # If we get here there must be at least 1 more line to write.
                    f.write(newline_character)
                    line_counter += 1
                    i += 1
                    extra_lines_done = True

                # Necessary otherwise the next condition would never be
                # satisifed.
                line_counter -= 1

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
            if i >= len(lines):
                loop = False
            # Continue looping if there are still extra lines to write.
            if put_at_line_number > len(lines) and not extra_lines_done:
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
    :raises: LineOutOfFileBoundsError or the built-in exceptions.

    .. note::
         It is possible to remove a single line only. This happens when
         the parameters delete_line_from and delete_line_to are equal.
    """
    # At least one line must be deleted.
    # Base case delete_line_to - delete_line_from == 0, corresponds to a
    # single line.
    assert delete_line_to - delete_line_from >= 0
    assert delete_line_from >= 1
    assert delete_line_to >= 1

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Invalid line range.
    if delete_line_from > len(lines) or delete_line_to > len(lines):
        raise LineOutOfFileBoundsError

    line_counter = 1
    # Rewrite the file without the string.
    with open(output_file, 'w') as f:
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
