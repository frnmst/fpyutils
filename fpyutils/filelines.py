#

"""Functions on reading and writing files by line."""

from .exceptions import (LineOutOfFileBoundsError)


def get_line_matches(input_file,
                     pattern,
                     max_occurrencies,
                     loose_matching=True):
    """Get the line numbers of matched patterns.

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
    :raises: LineOutOfFileBoundsError or FileNotFoundError

    .. warning:: The parameter max_occurrencies must be greater than
        zero.

    .. note:: To get all occurrencies of a pattern, the parameter
        max_occurrencies must be set to ``float('inf')``.

    :Example:

    >>> import fpyutils
    >>> fpyutils.get_line_matches('foo.txt','bar',5)
    {1: 8, 2: 17}
    """
    assert isinstance(input_file, str)
    assert isinstance(pattern, str)
    assert (isinstance(max_occurrencies, int)
            or isinstance(max_occurrencies, float))
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
        while (line
                and float(occurrency_counter) < float(max_occurrencies)):
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
    """Write a string at the specified line.

    Keyword arguments
    input_file -- the file that needs to be read
    string_to_be_inserted -- the string that needs to be added
    line_number -- the line number on which to append the string
    output_file -- the file that needs to be written with the new content
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
    """Remove a line interval.

    Keyword arguments
    input_file -- the file that needs to be read
    line_from -- the line number from which start deleting
    line_to -- the line number to which stop deleting
    output_file -- the file that needs to be written without the
    selected lines
    """
    assert isinstance(input_file, str)
    assert isinstance(line_from, int)
    assert isinstance(output_file, str)
    assert isinstance(line_to, int)
    # At least one line must be deleted.
    assert line_to - line_from >= 1
    assert line_from > 0
    assert line_to > 0

    # 1. Read the whole file.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 2. Save the total lines.
    total_lines = len(lines)

    # 3. Raise an exception if we are trying to delete an invalid line.
    if (line_from > total_lines
            or line_to > total_lines):
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
