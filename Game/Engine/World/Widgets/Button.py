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
from Engine.Utilities.General import RenderText
from Engine.World.Concepts.Node import Node

##
#
# The main class.
#
##

class Button(Node):

	def __init__(self, scene, text, font):

		super().__init__(scene, None, 3)

		self._text = text
		self._font = font

		self.ReplaceSprite(SpriteInstance(Sprite(RenderText(self._text, font))))