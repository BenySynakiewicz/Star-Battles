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
from Engine.Utilities.General import RenderText
from Engine.World.Concepts.Node import Node

from pygame import mouse

##
#
# The main class.
#
##

class Button(Node):

	def __init__(self, scene, text, font, inactiveColor = Color.White, activeColor = Color.Blue):

		super().__init__(scene, None, 3)

		# Initialize the member variables.

		self._text = text
		self._font = font

		self._inactiveColor = inactiveColor
		self._activeColor = activeColor

		self._inactiveSprite = None
		self._activeSprite = None

		self._shownSpriteIsActive = False

		# Generate the sprite.

		self._GenerateSprite()
		self.ReplaceSprite(self._inactiveSprite)

	def IsBeingPointedAt(self):

		mouseCursorPosition = mouse.get_pos()
		rectangle = self.GetRectangle()

		return rectangle.collidepoint(mouseCursorPosition)

	def _GenerateSprite(self):

		activeSurface = RenderText(self._text, self._font, self._activeColor)
		self._activeSprite = Sprite(activeSurface)

		inactiveSurface = RenderText(self._text, self._font, self._inactiveColor)
		self._inactiveSprite = Sprite(inactiveSurface)

	# Inherited methods.

	def Update(self, milisecondsPassed):

		isBeingPointedAt = self.IsBeingPointedAt()

		if isBeingPointedAt and not self._shownSpriteIsActive:

			self._shownSpriteIsActive = True
			self.ReplaceSprite(self._activeSprite)

		elif not isBeingPointedAt and self._shownSpriteIsActive:

			self._shownSpriteIsActive = False
			self.ReplaceSprite(self._inactiveSprite)