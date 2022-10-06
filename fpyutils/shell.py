# -*- coding: utf-8 -*-
#
# shell.py
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
"""Functions on shell."""

import subprocess
import sys


def execute_command_live_output(
        command: str,
        shell: str = '/bin/bash',
        dry_run: bool = False,
        output_character_encoding: str = 'UTF-8') -> int:
    r"""Execute and print the output of a command relatime.

    :parameter command: the shell commands that needs to be executed.
    :parameter shell: the shell binary that will be used to execute the command.
         Defaults to ``/bin/bash``.
    :parameter dry_run: print the command instead of executing it.
         Defaults to ``False``.
    :parameter output_character_encoding: the character encoding of the output.
         Defaults to ``UTF-8``.
    :type command: str
    :type shell: str
    :type dry_run: bool
    :type output_character_encoding: str
    :returns: process.returncode, the return code of the executed command.
    :rtype: int
    :raises: a subprocess, sys or a built-in exception.
    """
    # See https://stackoverflow.com/a/53811881
    #
    # Copyright (C) 2018 Tom Hale @ Stack Exchange (https://stackoverflow.com/a/53811881)
    # Copyright (C) 2020 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
    #
    # This script is licensed under a
    # Creative Commons Attribution-ShareAlike 4.0 International License.
    #
    # You should have received a copy of the license along with this
    # work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

    retval: int
    if dry_run:
        print(shell + ' -c ' + command)
        retval = 0
    else:
        # See also https://stackoverflow.com/questions/7407667/python-subprocess-subshells-and-redirection/7407744
        # and https://stackoverflow.com/a/58696973
        with subprocess.Popen([shell, '-c', command],
                              stderr=subprocess.PIPE) as process:

            go: bool = True
            while go:
                output: str = process.stderr.readline().decode(
                    output_character_encoding)
                if output == str() and process.poll() is not None:
                    go = False
                if go and output != str():
                    sys.stdout.write(output)
                    sys.stdout.flush()
            retval = process.returncode

    return retval


if __name__ == '__main__':
    pass
