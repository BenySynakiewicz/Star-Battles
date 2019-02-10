##
#
# Star Battles
# Copyright (C) (2019) Beny Synakiewicz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##

##
#
# Imports.
#
##

from pathlib import Path
from string import Template

from natsort import natsorted, ns

##
#
# Functions.
#
##

def FindFiles(path = None, recursively = False, suffixes = None):

	path = path if isinstance(path, Path) else Path(path or ".")
	allFiles = [file for file in path.glob("**/*" if recursively else "*") if file.is_file()]

	suffixes = [suffix.lower() for suffix in suffixes] if suffixes else None
	files = allFiles if not suffixes else [file for file in allFiles if file.suffix.lower() in suffixes]

	return natsorted(files, key = lambda path: str(path), alg = ns.IGNORECASE)

def SubstituteInPath(path, identifier, value):

	return Path(Template(str(path)).substitute({identifier: value}))