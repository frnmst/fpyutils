from fpyutils import (filelines, exceptions)
import string
import random
import unittest
from unittest.mock import patch, mock_open
import sys

# Note:
# To preserve the success of the tests,
# these generate_* functions are
# not to be modified.
def generate_fake_file_as_string():
    DATA_TO_BE_READ = '''# One\n## One.Two\n'''

    return DATA_TO_BE_READ

def generate_fake_file_with_matches_as_string():
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


class TestLines(unittest.TestCase):

    def test_get_line_matches(self):
        # Test 0 pattern matches.
        with patch('builtins.open', mock_open(read_data=generate_fake_file_as_string())) as m:
            matches = filelines.get_line_matches(input_file='foo.md',
                                                 pattern='[](TOC)',
                                                 number_of_occurrencies=1)

        self.assertTrue(1 not in matches)

        # Test >= 1 pattern match.
        with patch('builtins.open', mock_open(read_data=generate_fake_file_with_matches_as_string())) as m:
            matches = filelines.get_line_matches(input_file='foo.md',
                                                 pattern='[](TOC)',
                                                 number_of_occurrencies=2**32)

        self.assertEqual(matches[1],4)
        self.assertEqual(matches[2],10)
        self.assertTrue(3 not in matches)

    def test_insert_string_at_line(self):
        string_to_be_inserted = "Some string_to_be_inserted"

        # Insert string_to_be_inserted in an existing line.
        line_no=2
        buff = generate_fake_file_as_string()

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

        # Insert string_to_be_inserted in a non-existing line. We simply have to check if the
        # correct exception is raised.
        line_no=2**32

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch('builtins.open', mock_open(read_data=generate_fake_file_as_string())) as m:
                filelines.insert_string_at_line('foo.md', string_to_be_inserted, line_no, 'foo.md')

        # Same as prevous case but this is an always-true condition.
        line_no=0

        with self.assertRaises(exceptions.LineOutOfFileBoundsError):
            with patch('builtins.open', mock_open(read_data=generate_fake_file_as_string())) as m:
                filelines.insert_string_at_line('foo.md', string_to_be_inserted, line_no, 'foo.md')

    def test_remove_string_at_line(self):
#        remove_string_at_line(input_file, line_from, line_to, output_file)
        pass
        # TODO

if __name__ == '__main__':
    unitttest.main()
