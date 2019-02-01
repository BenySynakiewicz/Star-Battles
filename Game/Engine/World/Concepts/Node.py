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

from Engine.Core.Resources import Resources
from Engine.Media.SpriteInstance import SpriteInstance
from Engine.Utilities.Vector import Vector
from Engine.Utilities.General import GetScreen
from Engine.World.Utilities.Positioning import IsOutsideScreen
from Engine.World.Utilities.Timed import Timed

from copy import copy

from pygame import Rect

##
#
# The main class.
#
##

class Node(Timed):

	def __init__(self, scene, sprite, zIndex = 0):

		super().__init__()

		self._scene = scene
		self._terminated = False

		self._sprite = SpriteInstance(Resources().GetSprite(sprite))
		self._zIndex = zIndex

		self._position = Vector()
		self._dimensions = self._sprite.GetDimensions()

	def GetPosition(self):

		return self._position

	def GetDimensions(self):

		return self._dimensions

	def IsTerminated(self):

		return self._terminated

	def DoesCollideWith(self, other):

		if self == other:
			return False

		rectangle = Rect(tuple(self._position), tuple(self._dimensions))
		otherRectangle = Rect(tuple(other._position), tuple(other._dimensions))

		if not rectangle.colliderect(otherRectangle):
			return False

		mask = self._sprite.GetMask()
		otherMask = other._sprite.GetMask()

		offsetX = rectangle[0] - otherRectangle[0]
		offsetY = rectangle[1] - otherRectangle[1]

		return otherMask.overlap(mask, (offsetX, offsetY))

	def ReplaceSprite(self, sprite, loop = True):

		self._sprite = SpriteInstance(Resources().GetSprite(sprite), loop)

		self._position += self._dimensions // 2
		self._dimensions = self._sprite.GetDimensions()
		self._position -= self._dimensions // 2

	def SetPosition(self, position):

		self._position = copy(position)

	def SetRelativePosition(self, node, relation):

		self._position = relation(node._position, node._dimensions, self._dimensions)

	def Terminate(self):

		self._terminated = True

		self.OnTermination()

	def Update(self, milisecondsPassed):

		self._sprite.Update(milisecondsPassed)
		self.UpdateTimers(milisecondsPassed)

		if IsOutsideScreen(self._position, self._dimensions):
			self.Terminate()

	def Render(self):

		self._sprite.Blit(GetScreen(), self._position)

	def OnCollision(self, node):

		pass

	def OnTermination(self):

		pass