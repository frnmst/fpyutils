#
# yaml.py
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
"""Functions on YAML."""

import yaml


def load_configuration(configuration_file: str) -> dict:
    r"""Load YAML data from a configuration file.

    :parameter configuration_file: the file that needs to be read.
    :type configuration_file: str
    :returns: data, a dictionary corresponding to the YAML data.
    :rtype: dict
    :raises: a yaml or built-in exception.
    """
    with open(configuration_file, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    return data


if __name__ == '__main__':
    pass
