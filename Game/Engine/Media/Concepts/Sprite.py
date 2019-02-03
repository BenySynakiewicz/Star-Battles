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
from Engine.Media.Utilities.SurfaceProcessor import InterpolateToDimensions, InterpolateToScale
from Engine.Utilities.General import Blit, FindFiles, GetDimensions

from copy import copy
from pathlib import Path

from pygame import image, mask, surfarray, transform

##
#
# The main class.
#
##

class Sprite:

	def __init__(self, path, shadows: bool = False, framesPerSecond: int = 40):

		path = Path(path)
		filePaths = FindFiles(path, recursively = False, suffixes = [".png"]) if path.is_dir() else [path]

		self._surfaces = [image.load(str(filePath)).convert_alpha() for filePath in filePaths]
		self._masks = [mask.from_surface(surface) for surface in self._surfaces]

		self._framesPerSecond = framesPerSecond

		self._shadows = None
		if shadows:
			self.CreateShadow()

	def CreateShadow(self):

		if self._shadows:
			return

		self._shadows = [InterpolateToScale(surface, 1.05) for surface in self._surfaces]

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

	def GetRotatedCopy(self, angle):

		rotatedCopy = copy(self)

		rotatedCopy._surfaces = [transform.rotate(surface, angle) for surface in rotatedCopy._surfaces]
		rotatedCopy._masks = [mask.from_surface(surface) for surface in self._surfaces]

		if rotatedCopy._shadows:
			rotatedCopy._shadows = None
			rotatedCopy.CreateShadow()

		return rotatedCopy

	def GetScaledCopy(self, dimensions):

		scaledCopy = copy(self)

		scaledCopy._surfaces = [InterpolateToDimensions(surface, dimensions) for surface in scaledCopy._surfaces]
		scaledCopy._masks = [mask.from_surface(surface) for surface in self._surfaces]

		if scaledCopy._shadows:
			scaledCopy._shadows = None
			scaledCopy.CreateShadow()

		return scaledCopy

	def Blit(self, frame, surface, position):

		if self._shadows:
			Blit(surface, self._shadows[frame], position + Parameters.ShadowDistance)

		Blit(surface, self._surfaces[frame], position)