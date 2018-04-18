#
# tests.py
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
"""Tests."""

from fpyutils import (filelines, exceptions)
import unittest
from unittest.mock import patch, mock_open


class TestFileLines(unittest.TestCase):
    """filelines modules test."""

    # Note:
    # To preserve the success of the tests,
    # these generate_* methods are
    # not to be modified.
    def generate_fake_file_as_string(self):
        """Generate static data."""
        DATA_TO_BE_READ = '''\
# One\n\
## One.Two\n\
'''

        return DATA_TO_BE_READ

    def generate_fake_file_with_matches_as_string(self):
        """Generate static data."""
        DATA_TO_BE_READ = '''\
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
        return DATA_TO_BE_READ

    def test_get_line_matches_zero_pattern_matches(self):
        """test_get_line_matches_zero_pattern_matches."""
        with patch(
                'builtins.open',
                mock_open(read_data=self.generate_fake_file_as_string())):
            matches = filelines.get_line_matches(
                input_file='foo.md', pattern='[](TOC)', max_occurrencies=1)

        self.assertTrue(1 not in matches)

    def test_get_line_matches_more_than_zero_pattern_matches(self):
        """test_get_line_matches_more_than_zero_pattern_matches."""
        with patch(
                'builtins.open',
                mock_open(read_data=self.
                          generate_fake_file_with_matches_as_string())):
            matches = filelines.get_line_matches(
                input_file='foo.md', pattern='[](TOC)', max_occurrencies=2**32)

        self.assertEqual(matches[1], 4)
        self.assertEqual(matches[2], 10)
        self.assertTrue(3 not in matches)

    def test_get_line_matches_zero_pattern_matches_with_loose_matching_disabled(
            self):
        """test_get_line_matches_zero_pattern_matches_with_loose_matching_disabled."""
        with patch(
                'builtins.open',
                mock_open(read_data=self.
                          generate_fake_file_with_matches_as_string())):
            matches = filelines.get_line_matches(
                input_file='foo.md',
                pattern='[](TOC)',
                max_occurrencies=2**32,
                loose_matching=False)

        self.assertTrue(1 not in matches)

    def test_get_line_matches_more_than_zero_pattern_matches_with_loose_matching_disabled(
            self):
        """test_get_line_matches_more_than_zero_pattern_matches_with_loose_matching_disabled."""
        with patch(
                'builtins.open',
                mock_open(read_data=self.
                          generate_fake_file_with_matches_as_string())):
            matches = filelines.get_line_matches(
                input_file='foo.md',
                pattern='[](TOC)\n',
                max_occurrencies=2**32,
                loose_matching=False)

        self.assertEqual(matches[1], 4)
        self.assertEqual(matches[2], 10)
        self.assertTrue(3 not in matches)

    def _test_insert_string_at_line_in_existing_line(self, append):
        """test_insert_string_at_line_in_existing_line."""
        string_to_be_inserted = "Some string_to_be_inserted"

        line_no = 2
        buff = self.generate_fake_file_as_string()

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

            if line_counter == line_no:
                # At most one write operation must be done in this manner.
                if append:
                    handle.write.assert_any_call(line + string_to_be_inserted)
                else:
                    handle.write.assert_any_call(string_to_be_inserted + line)
            else:
                handle.write.assert_any_call(line)
            line_counter += 1

    def test_insert_string_at_line_in_existing_line(self):
        self._test_insert_string_at_line_in_existing_line(append=True)
        self._test_insert_string_at_line_in_existing_line(append=False)

    def test_insert_string_at_line_in_non_existing_line(self):
        """test_insert_string_at_line_in_non_existing_line."""
        # We simply have to check if the correct exception is raised.
        string_to_be_inserted = "Some string_to_be_inserted"
        line_no = 2**32

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch(
                    'builtins.open',
                    mock_open(read_data=self.generate_fake_file_as_string())):
                filelines.insert_string_at_line(
                    'foo.md', string_to_be_inserted, line_no, 'foo.md')

    def test_remove_line_interval_existing_interval(self):
        """test_remove_line_interval_existing_interval."""
        # Assert called with everything except the missing lines.
        line_from = 5
        line_to = 9
        buff = self.generate_fake_file_with_matches_as_string()

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

    def test_remove_line_interval_non_existing_interval(self):
        """test_remove_line_interval_non_existing_interval."""
        # We simply have to check if the correct exception is raised.
        line_from = 1
        line_to = 4

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch(
                    'builtins.open',
                    mock_open(read_data=self.generate_fake_file_as_string())):
                filelines.remove_line_interval('foo.md', line_from, line_to,
                                               'foo.md')


if __name__ == '__main__':
    unittest.main()
