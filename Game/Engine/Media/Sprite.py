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

from pygame import image, mask, surfarray

##
#
# The main class.
#
##

class Sprite:

	def __init__(self, path, createShadow: bool = False):

		self._surface = image.load(path).convert_alpha()
		self._mask = mask.from_surface(self._surface)
		self._shadowSurface = None

		if createShadow:
			self.CreateShadow()

	def CreateShadow(self):

		if self._shadowSurface:
			return

		self._shadowSurface = self._surface.copy()

		shadowPixelData = surfarray.pixels3d(self._shadowSurface)
		shadowPixelData[:] = 0
		
	def GetDimensions(self):

		return GetDimensions(self._surface)

	def GetMask(self):

		return self._mask

	def Blit(self, surface, position):

		if self._shadowSurface:
			Blit(surface, self._shadowSurface, position + Parameters.ShadowDistance)

		Blit(surface, self._surface, position)