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
from Engine.Utilities.Vector import Vector

from numpy import clip
from pygame import image, mask, Surface, surfarray, transform, SRCALPHA

##
#
# The main class.
#
##

class SpriteInstance:

	def __init__(self, sprite, loop = True):

		self._sprite = sprite

		self._loop = loop

		self._frame = 0
		self._sinceLatestFrame = 0

	def GetDimensions(self):

		return self._sprite.GetDimensions()

	def GetMask(self):

		return self._sprite.GetMask(self._frame)

	def IsFinished(self):

		return (not self._loop) and (self._sprite.GetFrameCount() - 1 == self._frame)

	def SetLooping(self, loop):

		self._loop = loop

	def Update(self, milisecondsPassed):

		if self.IsFinished():
			return

		self._sinceLatestFrame += milisecondsPassed

		frameDuration = 1000 / self._sprite.GetFramesPerSecond()
		framesPassed = int(self._sinceLatestFrame / frameDuration)

		if not framesPassed:
			return
		else:
			self._sinceLatestFrame = 0

		self._frame = self._frame + framesPassed

		frameCount = self._sprite.GetFrameCount()
		if (self._frame > frameCount - 1):
			self._frame = (frameCount - 1) if not self._loop else (self._frame % frameCount)

	def Blit(self, surface, position):

		self._sprite.Blit(self._frame, surface, position)