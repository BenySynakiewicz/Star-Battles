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

from Engine.Utilities.Color import InterpolateBetweenColors
from Engine.Utilities.Rendering import RenderRoundedRectangle
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Widget import Widget

from pygame import (
	draw,
	Rect, Surface,
	SRCALPHA,
)

##
#
# The main class.
#
##

class Bar(Widget):

	# The constructor.

	def __init__(self, scene, color, colorOnFull, targetDimensions, interpolateColors = False, rounded = False):

		super().__init__()

		# Initialize the member variables.

		self._surface = None

		self._color = color
		self._colorOnFull = colorOnFull
		self._targetDimensions = targetDimensions

		self._interpolateColors = interpolateColors
		self._rounded = rounded

		self._progress = 100

		# Generate (and set) the surfaces.

		self._GenerateSurface()

	# Operations.

	def SetProgress(self, progress):

		if progress != self._progress:

			self._progress = progress

			self._GenerateSurface()

	# Utilities.

	def _GenerateSurface(self):

		# Create the surface.

		self._surface = Surface(self._targetDimensions, SRCALPHA)

		# Draw the bar.

		if not self._interpolateColors:
			currentColor = self._colorOnFull if (100 == self._progress) else self._color
		else:
			currentColor = InterpolateBetweenColors(self._color, self._colorOnFull, self._progress / 100.0)

		area = Vector(self._targetDimensions.X * (self._progress / 100), self._targetDimensions.Y)

		if self._rounded:
			RenderRoundedRectangle(self._surface, tuple(Vector()), tuple(area), currentColor, 1.0)
		else:
			draw.rect(self._surface, currentColor, Rect((0, 0), tuple(area)))

		# Set the surface as the current surface.

		self.SetSurface(self._surface)