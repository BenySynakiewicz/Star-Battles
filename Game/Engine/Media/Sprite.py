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

from copy import copy

from pygame import image, mask, surfarray, transform

##
#
# The main class.
#
##

class Sprite:

	def __init__(self, paths, shadows: bool = False, framesPerSecond: int = 40):

		self._surfaces = [image.load(path).convert_alpha() for path in paths]
		self._masks = [mask.from_surface(surface) for surface in self._surfaces]
		self._shadows = None

		self._framesPerSecond = framesPerSecond

		if shadows:
			self.CreateShadow()

	def CreateShadow(self):

		if self._shadows:
			return

		shadowDimensions = self.GetDimensions() * 1.025
		shadowDimensions.X = int(shadowDimensions.X)
		shadowDimensions.Y = int(shadowDimensions.Y)

		self._shadows = [transform.smoothscale(surface, tuple(shadowDimensions)) for surface in self._surfaces]

		for shadow in self._shadows:
			surfarray.pixels3d(shadow)[:] = 0
		
	def GetDimensions(self):

		return GetDimensions(self._surfaces[0])

	def GetMask(self, frame):

		return self._masks[frame]

	def GetFrameCount(self):

		return len(self._surfaces)

	def GetFramesPerSecond(self):

		return self._framesPerSecond

	def GetScaledCopy(self, dimensions):

		scaledCopy = copy(self)

		scaledCopy._surfaces = [transform.smoothscale(surface, tuple(dimensions)) for surface in scaledCopy._surfaces]
		scaledCopy._masks = [mask.from_surface(surface) for surface in self._surfaces]

		scaledCopy._shadows = None
		scaledCopy.CreateShadow()

		return scaledCopy

	def Blit(self, frame, surface, position):

		if self._shadows:
			Blit(surface, self._shadows[frame], position + Parameters.ShadowDistance)

		Blit(surface, self._surfaces[frame], position)