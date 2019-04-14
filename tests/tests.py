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
import tempfile
import pathlib

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

    def _test_helper_insert_string_at_line(self, append, buff,
                                           string_to_be_inserted, line_no):
        with tempfile.TemporaryDirectory() as d:
            filename = str(pathlib.PurePath(d, 'testing'))
            with open(filename, 'w') as f:
                f.write(buff)
                f.flush()

            filelines.insert_string_at_line(filename, string_to_be_inserted,
                                            line_no, filename, append)

            with open(filename, 'r') as f:
                content = f.read()

        return content

    def test_insert_string_at_line(self):
        """Test insert_string_at_line."""
        string_to_be_inserted = "Some string_to_be_inserted"
        buff = FAKE_FILE_AS_STRING

        # existing line.
        line_no = 2
        append = False
        result = self._test_helper_insert_string_at_line(
            append, buff, string_to_be_inserted, line_no)
        expected = buff.split('\n')[
            0] + '\n' + string_to_be_inserted + buff.split('\n')[1] + '\n'
        self.assertEqual(expected, result)

        line_no = 2
        append = True
        result = self._test_helper_insert_string_at_line(
            append, buff, string_to_be_inserted, line_no)
        expected = buff.split('\n')[0] + '\n' + buff.split(
            '\n')[1] + '\n' + string_to_be_inserted
        self.assertEqual(expected, result)

        # non existing line.
        line_no = 2**5
        # We do not need to consider the last component of the buff.split() list.
        number_of_newlines_after_last_existing_line = line_no - (
            len(buff.split('\n')) - 1)
        append = False
        result = self._test_helper_insert_string_at_line(
            append, buff, string_to_be_inserted, line_no)
        expected = buff.split('\n')[0] + '\n' + buff.split(
            '\n'
        )[1] + number_of_newlines_after_last_existing_line * '\n' + string_to_be_inserted
        self.assertEqual(expected, result)

        line_no = 2**5
        number_of_newlines_after_last_existing_line = line_no - (
            len(buff.split('\n')) - 1)
        append = True
        result = self._test_helper_insert_string_at_line(
            append, buff, string_to_be_inserted, line_no)
        expected = buff.split('\n')[0] + '\n' + buff.split(
            '\n'
        )[1] + number_of_newlines_after_last_existing_line * '\n' + string_to_be_inserted
        self.assertEqual(expected, result)

    def _test_helper_remove_line_interval(self, buff, line_from, line_to):
        with tempfile.TemporaryDirectory() as d:
            filename = str(pathlib.PurePath(d, 'testing'))
            with open(filename, 'w') as f:
                f.write(buff)
                f.flush()

            filelines.remove_line_interval(filename, line_from, line_to,
                                           filename)

            with open(filename, 'r') as f:
                content = f.read()

        return content

    def test_remove_line_interval(self):
        """test_remove_line_interval."""
        # remove_line_interval existing interval.
        # Assert called with everything except the missing lines.
        line_from = 5
        line_to = 9
        buff = FAKE_FILE_WITH_MATCHES_AS_STRING
        result = self._test_helper_remove_line_interval(
            buff, line_from, line_to)
        # Also add missing newline after the join operation.
        expected = '\n'.join(
            buff.split('\n')[0:line_from - 1] +
            buff.split('\n')[line_to:-1]) + '\n'
        self.assertEqual(expected, result)

        # remove_line_interval non existing interval.
        # We simply have to check if the correct exception is raised.
        line_from = 1
        line_to = 4
        buff = FAKE_FILE_AS_STRING
        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            self._test_helper_remove_line_interval(buff, line_from, line_to)

        # Negative line range.
        line_from = 4
        line_to = 1
        buff = FAKE_FILE_AS_STRING
        with self.assertRaises(exceptions.NegativeLineRangeError):
            self._test_helper_remove_line_interval(buff, line_from, line_to)


if __name__ == '__main__':
    unittest.main()
