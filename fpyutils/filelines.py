#!/usr/bin/env python3

from .exceptions import (LineOutOfFileBoundsError)

#
# Functions on reading and writing files by line.
#


def get_line_matches(input_file,
                     pattern,
                     number_of_occurrencies,
                     loose_matching=True):
    """ Get the line numbers for the matched patterns.
        A match exists if a pattern corresponds exactly to the
        content of a line of the input file.

        Returns: a dict corresponding to the matches. If no match is found for
                 that particular occurrency, the function does not set the dict
                 key.
    """

    assert isinstance(input_file, str)
    assert isinstance(pattern, str)
    assert isinstance(number_of_occurrencies, int)

    occurrency_counter = 0
    occurrency_matches = dict()

    # 1. Strip all whitespaces from pattern if requested.
    if loose_matching:
        pattern = pattern.strip()

    line_number = 1
    with open(input_file, 'r') as f:
        # 2. Read the first line.
        line = f.readline()
        while line:
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


def insert_string_at_line(input_file,
                          string_to_be_inserted,
                          line_number,
                          output_file):
    """ Put the string_to_be_inserted on the specified line number line_number.
        Since we are doing a rw operation, it is possbile that
        input and output are done on different files.

        Returns: None
    """

    assert isinstance(input_file, str)
    assert isinstance(string_to_be_inserted, str)
    assert isinstance(line_number, int)
    assert isinstance(output_file, str)

    # 1. Read the whole file.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 2. Raise an exception if we are trying to write on a non-existing line.
    if line_number > len(lines) or line_number <= 0:
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


def remove_string_at_line(input_file, line_from, line_to, output_file):
    """ Remove the specified line interval from input_file and write the result
        to output_file.
    """

    assert isinstance(input_file, str)
    assert isinstance(line_from, int)
    assert isinstance(output_file, str)
    assert isinstance(line_to, int)

    # 1. Read the whole file.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 2. Save the total lines.
    total_lines = len(lines)

    # 3. Raise an exception if we are trying to delete an invalid line
    #    or we are dealing with wrong input.
    if (line_from > line_to
            or line_from > total_lines
            or line_to > total_lines
            or line_from == line_to
            or line_from <= 0
            or line_to <= 0):
        raise LineOutOfFileBoundsError

    line_number = 1
    # 3. Rewrite the file without the toc.
    with open(output_file, 'w') as f:
        for line in lines:
            # Ignore the line interval where the toc lies.
            if line_number >= line_from and line_number <= line_to:
                pass
                # Write the rest of the file.
            else:
                f.write(line)
            line_number += 1


if __name__ == '__main__':
    pass
