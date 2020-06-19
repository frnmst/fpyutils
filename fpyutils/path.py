#
# path.py
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
"""Functions on paths."""

import pathlib
import re
import urllib
import datetime
import secrets
import hashlib


def get_last_path_component_from_url(url: str) -> str:
    r"""Transform a string to a datetime object."""
    return pathlib.Path(urllib.parse.urlsplit(url).path).name


def remove_component(element: str, pattern: str) -> str:
    r"""Remove a pattern from an element."""
    return re.split(pattern, element)[0]


def rebuild_uri(uri_base: str, path: str) -> str:
    """Rebuild a URI by a trailing forward slash if necessary and a path.

    ..note: see https://stackoverflow.com/a/59818095
    """
    if uri_base.endswith('/'):
        uri_base = uri_base
    else:
        uri_base = f"{uri_base}/"

    return uri_base + path


def gen_pseudorandom_path(path_suffix: str = str(),
                          date_component_format: str = '%F_%H-%M-%S_%f',
                          component_separator: str = '_',
                          pseudorandom_component_bytes: int = 4,
                          hash_component_digest_size: int = 3,
                          character_encoding: str = 'UTF-8') -> str:
    r"""Generate a string based on the current moment in time, a random token, a hash and some input.

    ..note:: this system minimises the risk of collisions for creating a path.
    """
    # 1. the current date.
    # call the fpyutils.datetime module.
    date_component = datetime.date.strftime(datetime.datetime.now(),
                                            date_component_format)

    # 2. a pseudorandom component.
    pseudorandom_component = secrets.token_urlsafe(
        nbytes=pseudorandom_component_bytes)

    # 3. a hash of path_suffix. This will be equal to
    #    'cec7ea' using blake2b and a digest size of 3.
    m = hashlib.blake2b(digest_size=hash_component_digest_size)
    m.update(path_suffix.encode(character_encoding))
    hashed_component = m.hexdigest()

    # 4. the path suffix, if present.
    if path_suffix != str():
        path_suffix = component_separator + path_suffix

    return (date_component + component_separator + pseudorandom_component +
            component_separator + hashed_component + path_suffix)


if __name__ == '__main__':
    pass
