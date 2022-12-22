# -*- coding: utf-8 -*-
#
# __init__.py
#
# Copyright (C) 2017-2021 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
"""Exposed API."""

from .exceptions import LineOutOfFileBoundsError, NegativeLineRangeError
from .filelines import (
    get_line_matches,
    insert_string_at_line,
    remove_line_interval,
)
from .notify import send_email, send_gotify_message
from .path import add_trailing_slash, gen_pseudorandom_path
from .shell import execute_command_live_output
