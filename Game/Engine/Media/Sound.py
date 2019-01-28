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

from pygame import mixer

##
#
# The main class.
#
##

class Sound:

	def __init__(self, path, channels):

		self._sound = mixer.Sound(str(path))
		self._channels = [mixer.Channel(x) for x in channels]


	def Play(self):

		channel = next(filter(lambda x: not x.get_busy(), self._channels), self._channels[0])
		channel.play(self._sound)