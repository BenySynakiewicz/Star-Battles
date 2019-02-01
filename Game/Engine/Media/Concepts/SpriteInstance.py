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

		self._baseSprite = sprite
		self._loop = loop

		self._rotation = None

		self._frame = 0
		self._timeSincePreviousFrame = 0

	def GetDimensions(self):

		return self._baseSprite.GetDimensions()

	def GetMask(self):

		return self._baseSprite.GetMask(self._frame)

	def IsFinished(self):

		return (not self._loop) and (self._baseSprite.GetFrameCount() - 1 == self._frame)

	def SetLooping(self, loop):

		self._loop = loop

	def SetRotation(self, rotation: int):

		self._rotation = rotation

	def Update(self, milisecondsPassed):

		if self.IsFinished():
			return

		self._timeSincePreviousFrame += milisecondsPassed
		framesPassed = self._timeSincePreviousFrame / (1000 / self._baseSprite.GetFramesPerSecond())

		if framesPassed < 1:
			return

		self._frame = int(self._frame + framesPassed)

		if self._frame > self._baseSprite.GetFrameCount() and not self._loop:
			self._frame = self._baseSprite.GetFrameCount() - 1
		else:
			self._frame = self._frame % self._baseSprite.GetFrameCount()

		self._timeSincePreviousFrame = 0

	def Blit(self, surface, position):

		if self._rotation:

			temporarySurface = Surface(tuple(self.GetDimensions()), SRCALPHA, 32)

			self._baseSprite.Blit(self._frame, temporarySurface, Vector())
			temporarySurface = transform.rotate(temporarySurface, self._rotation)

			Blit(surface, temporarySurface, position)

		else:

			self._baseSprite.Blit(self._frame, surface, position)