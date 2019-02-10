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
from Engine.Core.Resources import Resources
from Engine.Media.Concepts.Sprite import Sprite
from Engine.Media.Concepts.SpriteInstance import SpriteInstance
from Engine.Utilities.Color import Color
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, RenderText
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Node import Node

from pygame import mouse, gfxdraw, draw, Rect, Surface

##
#
# The main class.
#
##

class Button(Node):

	def __init__(self, scene, text, font, textColor = Color.White, backgroundColor = Color.Blue):

		super().__init__(scene, None)

		# Initialize the member variables.

		self._text = text
		self._font = font

		self._textColor = textColor
		self._backgroundColor = backgroundColor

		self._activeSprite = None
		self._inactiveSprite = None

		self._isActive = False

		# Generate and set the sprites.

		self._GenerateSprites()
		self.ReplaceSprite(self._inactiveSprite)

	def IsBeingPointedAt(self):

		mouseCursorPosition = mouse.get_pos()
		rectangle = self.GetRectangle()

		return rectangle.collidepoint(mouseCursorPosition)

	def _GenerateSprites(self):

		textSurface = RenderText(self._text, self._font, self._textColor)
		textSurfaceDimensions = GetDimensions(textSurface)

		radius = Vector(15, 15)

		textPosition = Vector(15, 5)
		surfaceDimensions = textSurfaceDimensions + (textPosition * 2)

		activeSurface = Surface(tuple(surfaceDimensions))
		gfxdraw.filled_polygon(activeSurface, (
			(0, radius.Y),
			(radius.X, 0),
			(surfaceDimensions.X - radius.X, 0),
			(surfaceDimensions.X, radius.Y),
			(surfaceDimensions.X, surfaceDimensions.Y - radius.Y),
			(surfaceDimensions.X - radius.X, surfaceDimensions.Y),
			(radius.X, surfaceDimensions.Y),
			(0, surfaceDimensions.Y - radius.Y),
		), self._backgroundColor)

		inactiveSurface = Surface(tuple(surfaceDimensions))

		activeSurface.set_alpha(32)
		Blit(inactiveSurface, activeSurface)
		activeSurface.set_alpha(255)

		Blit(activeSurface, textSurface, textPosition)
		Blit(inactiveSurface, textSurface, textPosition)

		self._activeSprite = activeSurface
		self._inactiveSprite = inactiveSurface

	# Inherited methods.

	def Update(self, milisecondsPassed):

		self._isActive = self.IsBeingPointedAt()

	def Render(self):

		Blit(GetScreen(), self._activeSprite if self._isActive else self._inactiveSprite, self._position)