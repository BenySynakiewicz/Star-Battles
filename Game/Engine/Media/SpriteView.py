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

from Engine.Core.Parameters import Parameters
from Engine.Utilities.General import Blit, GetDimensions

from numpy import clip
from pygame import image, mask, surfarray

##
#
# The main class.
#
##

class SpriteView:

	def __init__(self, sprite, loop = True):

		self._sprite = sprite
		self._loop = loop

		self._frame = 0
		self._timeSincePreviousFrame = 0

	def GetDimensions(self):

		return self._sprite.GetDimensions()

	def GetMask(self):

		return self._sprite.GetMask(self._frame)

	def IsFinished(self):

		return (not self._loop) and (self._sprite.GetFrameCount() - 1 == self._frame)

	def Blit(self, surface, position):

		self._sprite.Blit(self._frame, surface, position)

	def Update(self, milisecondsPassed):

		if self.IsFinished():
			return

		self._timeSincePreviousFrame += milisecondsPassed
		framesPassed = self._timeSincePreviousFrame / (1000 / self._sprite.GetFramesPerSecond())

		if framesPassed < 1:
			return

		self._frame = int(self._frame + framesPassed)

		if self._frame > self._sprite.GetFrameCount() and not self._loop:
			self._frame = self._sprite.GetFrameCount() - 1
		else:
			self._frame = self._frame % self._sprite.GetFrameCount()

		self._timeSincePreviousFrame = 0