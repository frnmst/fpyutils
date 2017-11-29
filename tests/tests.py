#

from fpyutils import (filelines, exceptions)
import unittest
from unittest.mock import patch, mock_open


class TestLines(unittest.TestCase):

    # Note:
    # To preserve the success of the tests,
    # these generate_* methods are
    # not to be modified.
    def generate_fake_file_as_string(self):
        DATA_TO_BE_READ = '''\
# One\n\
## One.Two\n\
'''

        return DATA_TO_BE_READ

    def generate_fake_file_with_matches_as_string(self):
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
        with patch('builtins.open',
                   mock_open(read_data=self.generate_fake_file_as_string())
                   ):
            matches = filelines.get_line_matches(input_file='foo.md',
                                                 pattern='[](TOC)',
                                                 max_occurrencies=1)

        self.assertTrue(1 not in matches)

    def test_get_line_matches_more_than_zero_pattern_matches(self):
        with patch('builtins.open',
                   mock_open(
                       read_data=self.generate_fake_file_with_matches_as_string())
                   ):
            matches = filelines.get_line_matches(input_file='foo.md',
                                                 pattern='[](TOC)',
                                                 max_occurrencies=2**32)

        self.assertEqual(matches[1], 4)
        self.assertEqual(matches[2], 10)
        self.assertTrue(3 not in matches)

    def test_get_line_matches_zero_pattern_matches_with_loose_matching_disabled(self):
        with patch('builtins.open', mock_open(read_data=self.generate_fake_file_with_matches_as_string())):
            matches = filelines.get_line_matches(input_file='foo.md',
                                                 pattern='[](TOC)',
                                                 max_occurrencies=2**32,
                                                 loose_matching=False)

        self.assertTrue(1 not in matches)

    def test_get_line_matches_more_than_zero_pattern_matches_with_loose_matching_disabled(self):
        with patch('builtins.open', mock_open(read_data=self.generate_fake_file_with_matches_as_string())):
            matches = filelines.get_line_matches(input_file='foo.md',
                                                 pattern='[](TOC)\n',
                                                 max_occurrencies=2**32,
                                                 loose_matching=False)

        self.assertEqual(matches[1], 4)
        self.assertEqual(matches[2], 10)
        self.assertTrue(3 not in matches)

        #
        # Test the max_line parameter.... TODO
        #

    def test_insert_string_at_line_in_existing_line(self):
        string_to_be_inserted = "Some string_to_be_inserted"

        line_no = 2
        buff = self.generate_fake_file_as_string()

        with patch('builtins.open', mock_open(read_data=buff)) as m:
            filelines.insert_string_at_line('foo.md', string_to_be_inserted, line_no, 'foo_two.md')

        # Get a similar representation of what the readline function returns:
        # separate each line and place it into a list.
        lines = buff.split('\n')

        # Strip the last list element which would result in an extra newline
        # character. This exsists because the resul of separating an empty
        # string. See https://docs.python.org/3.6/library/stdtypes.html#str.split
        lines = lines[0:-1]

        # Get the mock.
        handle = m()

        line_counter = 1
        for line in lines:

            # Put the newline character at the end of the line.
            line = line + '\n'

            if line_counter == line_no:
                # At most one write operation must be done in this manner.
                handle.write.assert_any_call(line + string_to_be_inserted)
            else:
                handle.write.assert_any_call(line)
            line_counter += 1

    def test_insert_string_at_line_in_non_existing_line(self):
        # We simply have to check if the correct exception is raised.
        string_to_be_inserted = "Some string_to_be_inserted"
        line_no = 2 ** 32

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch('builtins.open', mock_open(read_data=self.generate_fake_file_as_string())) as m:
                filelines.insert_string_at_line('foo.md', string_to_be_inserted, line_no, 'foo.md')

    def test_remove_line_interval_existing_interval(self):
        # Assert called with everything except the missing lines.
        line_from = 5
        line_to = 9
        buff = self.generate_fake_file_with_matches_as_string()

        with patch('builtins.open',
        mock_open(read_data=buff)) as m:
            filelines.remove_line_interval('foo.md', line_from, line_to, 'foo.md')

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
        # We simply have to check if the correct exception is raised.
        line_from = 1
        line_to = 4

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch('builtins.open', mock_open(read_data=self.generate_fake_file_as_string())):
                filelines.remove_line_interval('foo.md', line_from, line_to, 'foo.md')


if __name__ == '__main__':
    unittest.main()
