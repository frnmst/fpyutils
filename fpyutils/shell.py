#
# shell.py
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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


def execute_command_live_output(command: str, shell: str = '/bin/bash') -> int:
    r"""Execute and print the output of a command relatime.

    :parameter command: the shell commands that needs to be executed.
    :parameter shell: the shell binary that will be used to execute the command.
         Defaults to ``/bin/bash``.
    :type command: str
    :type shell: str
    :returns: process.returncode, the return code of the executed command.
    :rtype: int
    :raises: a subprocess, sys or a built-in exception.
    """
    # See https://stackoverflow.com/a/53811881
    #
    # Copyright (C) 2018 Tom Hale @ Stack Exchange (https://stackoverflow.com/a/53811881)
    # Copyright (C) 2020 Franco Masotti <franco.masotti@live.com>
    #
    # This script is licensed under a
    # Creative Commons Attribution-ShareAlike 4.0 International License.
    #
    # You should have received a copy of the license along with this
    # work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

    # See also https://stackoverflow.com/questions/7407667/python-subprocess-subshells-and-redirection/7407744
    process = subprocess.Popen([shell, '-c', command], stderr=subprocess.PIPE)

    go = True
    while go:
        out = process.stderr.readline().decode('UTF-8')
        if out == str() and process.poll() is not None:
            go = False
        if go and out != str():
            sys.stdout.write(out)
            sys.stdout.flush()

    return process.returncode


if __name__ == '__main__':
    pass
