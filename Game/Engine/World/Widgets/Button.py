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

from Engine.Utilities.Color import Color
from Engine.Utilities.General import Blit, GetDimensions, RenderText
from Engine.Utilities.Rendering import RenderRoundedRectangle
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Widget import Widget

from pygame import Surface, SRCALPHA

##
#
# Globals.
#
##

Padding = Vector(15, 5)

##
#
# The main class.
#
##

class Button(Widget):

	# The constructor.

	def __init__(self, scene, text, font, textColor = Color.White, backgroundColor = Color.Blue):

		super().__init__()

		# Initialize the member variables.

		self._text = text
		self._font = font

		self._textColor = textColor
		self._backgroundColor = backgroundColor

		self._activeSurface = None
		self._inactiveSurface = None

		# Generate (and set) the surfaces.

		self._GenerateSprites()

	# Updating.

	def Update(self, milisecondsPassed):

		self.SetSurface(self._activeSurface if self.IsBeingPointedAt() else self._inactiveSurface)

	# Utilities.

	def _GenerateSprites(self):

		# Render the text itself.

		textSurface = RenderText(self._text, self._font, self._textColor)
		textSurfaceDimensions = GetDimensions(textSurface)

		# Create both surfaces.

		surfaceDimensions = textSurfaceDimensions + (Padding * 2)

		self._activeSurface = Surface(tuple(surfaceDimensions), SRCALPHA)
		self._inactiveSurface = self._activeSurface.copy()

		RenderRoundedRectangle(self._activeSurface, Vector(), surfaceDimensions, (50, 50, 255, 255))
		RenderRoundedRectangle(self._inactiveSurface, Vector(), surfaceDimensions, (50, 50, 255, 32))

		# Draw text on both surfaces.

		Blit(self._activeSurface, textSurface, Padding)
		Blit(self._inactiveSurface, textSurface, Padding)

		# Set the inactive surface as the current surface.

		self.SetSurface(self._inactiveSurface)