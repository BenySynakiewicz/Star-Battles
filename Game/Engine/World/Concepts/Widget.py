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

from Engine.Utilities.General import Blit, GetDimensions, GetScreen
from Engine.Utilities.Vector import Vector

from pygame import mouse, Rect

##
#
# The main class.
#
##

class Widget:

	# The constructor.

	def __init__(self):

		self._surface = None

		self._position = Vector()
		self._dimensions = Vector()

	# Accessors.

	def GetPosition(self): return self._position
	def GetDimensions(self): return self._dimensions

	# Operations.

	def SetPosition(self, position):

		self._position = position

	def SetSurface(self, surface):

		self._surface = surface
		self._dimensions = GetDimensions(self._surface)

	# Utilities.

	def IsBeingPointedAt(self):

		mouseCursorPosition = mouse.get_pos()
		rectangle = Rect(tuple(self.GetPosition()), tuple(self.GetDimensions()))

		return rectangle.collidepoint(mouseCursorPosition)

	# Rendering.

	def Render(self):

		Blit(GetScreen(), self._surface, self._position)