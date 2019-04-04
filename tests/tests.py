#
# tests.py
#
# Copyright (C) 2017-2019 frnmst (Franco Masotti) <franco.masotti@live.com>
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
"""Tests."""

from fpyutils import (filelines, exceptions)
import unittest
from unittest.mock import (patch, mock_open)

# filelines module.
FAKE_FILE_AS_STRING = '''\
# One\n\
## One.Two\n\
'''
FAKE_FILE_WITH_MATCHES_AS_STRING = '''\
# One\n\
## One.Two\n\
Hello, this is some content\n\
[](TOC)\n\
This is some more content\n\
Bye\n\
And again let there be\n\
more\n\
content.\n\
[](TOC)\n\
End of toc\n\
'''


class TestFileLines(unittest.TestCase):
    """filelines modules test."""

    def test_get_line_matches(self):
        """test_get_line_matches."""
        # Zero pattern matches.
        with patch('builtins.open', mock_open(read_data=FAKE_FILE_AS_STRING)):
            matches = filelines.get_line_matches(
                input_file='foo.md', pattern='[](TOC)', max_occurrencies=1)
        self.assertTrue(1 not in matches)

        # More than zero pattern matches.
        with patch('builtins.open',
                   mock_open(read_data=FAKE_FILE_WITH_MATCHES_AS_STRING)):
            matches = filelines.get_line_matches(
                input_file='foo.md', pattern='[](TOC)', max_occurrencies=0)
        self.assertEqual(matches[1], 4)
        self.assertEqual(matches[2], 10)
        self.assertTrue(3 not in matches)

        # Zero pattern matches with loose matching disabled.
        with patch('builtins.open',
                   mock_open(read_data=FAKE_FILE_WITH_MATCHES_AS_STRING)):
            matches = filelines.get_line_matches(
                input_file='foo.md',
                pattern='[](TOC)',
                max_occurrencies=0,
                loose_matching=False)
        self.assertTrue(1 not in matches)

        # More than zero pattern matches with loose matching disabled.
        with patch('builtins.open',
                   mock_open(read_data=FAKE_FILE_WITH_MATCHES_AS_STRING)):
            matches = filelines.get_line_matches(
                input_file='foo.md',
                pattern='[](TOC)\n',
                max_occurrencies=0,
                loose_matching=False)
        self.assertEqual(matches[1], 4)
        self.assertEqual(matches[2], 10)
        self.assertTrue(3 not in matches)

    def _test_insert_string_at_line_in_existing_line(self, append,
                                                     extra_lines):
        """See the test_insert_string_at_line_in_existing_line function."""
        string_to_be_inserted = "Some string_to_be_inserted"

        if extra_lines:
            line_no = 2**5
        else:
            line_no = 2
        buff = FAKE_FILE_AS_STRING

        with patch('builtins.open', mock_open(read_data=buff)) as m:
            filelines.insert_string_at_line('foo.md', string_to_be_inserted,
                                            line_no, 'foo_two.md', append)

        # Get a similar representation of what the readline function returns:
        # separate each line and place it into a list.
        lines = buff.split('\n')

        # Strip the last list element which would result in an extra newline
        # character. This exists because it is the result of separating an empty
        # string. See
        # https://docs.python.org/3.6/library/stdtypes.html#str.split
        lines = lines[0:-1]

        # Get the mock.
        handle = m()

        line_counter = 1
        for line in lines:

            # Put the newline character at the end of the line.
            line = line + '\n'

            if extra_lines and line_counter == len(lines) + 1:
                handle.write.assert_called_with('\n')

            if line_counter == line_no:
                # At most one write operation can be done in this manner.
                if append:
                    handle.write.assert_called_with(line +
                                                    string_to_be_inserted)
                else:
                    handle.write.assert_called_with(string_to_be_inserted +
                                                    line)
            else:
                # The mock might not refer to the order of the insructions
                # inside this loop
                handle.write.assert_any_call(line)

            line_counter += 1

    def test_insert_string_at_line(self):
        """test_insert_string_at_line."""
        # insert_string_at_line in existing line.
        self._test_insert_string_at_line_in_existing_line(
            append=False, extra_lines=False)
        self._test_insert_string_at_line_in_existing_line(
            append=True, extra_lines=False)

        # insert_string_at_line in non existing line.
        self._test_insert_string_at_line_in_existing_line(
            append=False, extra_lines=True)
        self._test_insert_string_at_line_in_existing_line(
            append=True, extra_lines=True)

    def test_remove_line_interval(self):
        """test_remove_line_interval."""
        # remove_line_interval existing interval.
        # Assert called with everything except the missing lines.
        line_from = 5
        line_to = 9
        buff = FAKE_FILE_WITH_MATCHES_AS_STRING

        with patch('builtins.open', mock_open(read_data=buff)) as m:
            filelines.remove_line_interval('foo.md', line_from, line_to,
                                           'foo.md')

        handle = m()

        lines = buff.split('\n')
        lines = lines[0:-1]

        line_counter = 1
        for line in lines:

            # Put the newline character at the end of the line.
            line = line + '\n'

            # Check that only the external part of the line interval would have
            # been written.
            if line_counter < line_from or line_counter > line_to:
                handle.write.assert_any_call(line)
            else:
                self.assertTrue(line not in m.mock_calls)

            line_counter += 1

        # remove_line_interval non existing interval.
        # We simply have to check if the correct exception is raised.
        line_from = 1
        line_to = 4

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch('builtins.open',
                       mock_open(read_data=FAKE_FILE_AS_STRING)):
                filelines.remove_line_interval('foo.md', line_from, line_to,
                                               'foo.md')


if __name__ == '__main__':
    unittest.main()
