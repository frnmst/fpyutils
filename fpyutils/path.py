# -*- coding: utf-8 -*-
#
# path.py
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
"""Functions on paths."""

import datetime
import hashlib
import pathlib
import secrets
import urllib


def add_trailing_slash(uri: str) -> str:
    r"""Add a trailing slash when needed.

    :param uri: a string, usually an URI.
    :type uri: str
    :returns uri: the input string with a trailing slash.
    :rtype: str
    :raises: a built-in exception.
    """
    if uri.endswith('/'):
        uri = uri
    else:
        uri = f"{uri}/"

    return uri


def gen_pseudorandom_path(path_suffix: str = str(),
                          date_component_format: str = '%F_%H-%M-%S_%f',
                          component_separator: str = '_',
                          pseudorandom_component_bytes: int = 4,
                          hash_component_digest_size: int = 3,
                          character_encoding: str = 'UTF-8') -> str:
    r"""Generate a pseudorandom string useful for paths.

    :param path_suffix: the final part of the string.
        Defaults to ``str()``.
    :param date_component_format: the format of the date component.
        Defaults to ``%F_%H-%M-%S_%f``.
    :param component_separator: an element that separates the various components.
        Defaults to ``_``.
    :param pseudorandom_component_bytes: the number of bytes of the pseudorandom components.
        Defaults to ``4``.
    :param hash_component_digest_size: the digest size of the hashed component.
        Defaults to ``3``.
    :param character_encoding: the character encoding of the hashed component.
        Defaults to ``UTF-8``.
    :type path_suffix: str
    :type date_component_format: str
    :type component_separator: str
    :type pseudorandom_component_bytes: int
    :type hash_component_digest_size: int
    :type character_encoding: str
    :returns:
    :rtype: str
    :raises: a built-in exception.

    .. note::
        This system minimises the risk of collisions for creating a path.
    """
    # 1. the current date.
    # call the fpyutils.datetime module.
    date_component: str = datetime.date.strftime(datetime.datetime.now(),
                                                 date_component_format)

    # 2. a pseudorandom component.
    pseudorandom_component: str = secrets.token_urlsafe(
        nbytes=pseudorandom_component_bytes)

    # 3. a hash of path_suffix. This will be equal to
    #    'cec7ea' using blake2b and a digest size of 3.
    m = hashlib.blake2b(digest_size=hash_component_digest_size)
    m.update(path_suffix.encode(character_encoding))
    hashed_component: str = m.hexdigest()

    # 4. the path suffix, if present.
    if path_suffix != str():
        path_suffix = component_separator + path_suffix

    return (date_component + component_separator + pseudorandom_component +
            component_separator + hashed_component + path_suffix)


if __name__ == '__main__':
    pass
