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
from Engine.Media.Concepts.Sprite import Sprite
from Engine.Media.Concepts.SpriteInstance import SpriteInstance
from Engine.Utilities.Vector import Vector
from Engine.Utilities.General import GetScreen
from Engine.World.Utilities.Positioning import IsOutsideScreen
from Engine.World.Utilities.Timed import Timed

from pygame import Rect, Surface

##
#
# The main class.
#
##

class Node(Timed):

	# The constructor.

	def __init__(self, scene, sprite = None, dimensions = None, rotation = None, movementVector = None, zIndex = 0):

		super().__init__()

		self._scene = scene

		self._name = type(self).__name__

		self._collisionClasses = set()
		self._collisionExceptions = set()
		self._terminated = False

		self._spriteName = sprite
		self._sprite = SpriteInstance(Resources().GetSprite(sprite, dimensions, rotation)) if self._spriteName else None

		self._position = Vector()
		self._dimensions = self._sprite.GetDimensions() if self._sprite else None

		self._movementVector = movementVector
		self._movementStopped = False
		self._movement = None

		self._zIndex = zIndex

	# Accessors.

	def IsTerminated(self): return self._terminated
	def GetName(self): return self._name
	def GetPosition(self): return self._position
	def GetDimensions(self): return self._dimensions
	def GetCollisions(self): return (self._collisionClasses, self._collisionExceptions)
	def GetMovementVector(self): return self._movementVector
	def GetZIndex(self): return self._zIndex

	# Utilities.

	def GetCenter(self):

		return self._position + (self._dimensions / 2)

	# Collision handling.

	def DoesCollideWith(self, other):

		if self == other:
			return False

		otherCollisionClasses, otherCollisionExceptions = other.GetCollisions()
		if not self._collisionClasses & otherCollisionClasses:
			return False

		name = type(self).__name__
		otherName = type(other).__name__
		if name in otherCollisionExceptions or otherName in self._collisionExceptions:
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

	# Sprite and geometry management.

	def ReplaceSprite(self, sprite, dimensions = None, rotation = None, loop = True):

		if isinstance(sprite, Surface): self._sprite = SpriteInstance(Sprite(sprite))
		elif isinstance(sprite, Sprite): self._sprite = SpriteInstance(sprite)
		elif isinstance(sprite, SpriteInstance): self._sprite = sprite
		else:
			self._spriteName = sprite
			self._sprite = SpriteInstance(
				Resources().GetSprite(self._spriteName, dimensions, rotation),
				currentFrame = self._sprite.GetCurrentFrame(),
				loop = loop
			)

		hadDimensions = bool(self._dimensions)

		if hadDimensions: self._position += self._dimensions / 2
		self._dimensions = self._sprite.GetDimensions()
		if hadDimensions: self._position -= self._dimensions / 2

	def SetPosition(self, position):

		self._position = Vector(*position)

	def SetRelativePosition(self, node, relation):

		self._position = relation(node._position, node._dimensions, self._dimensions)

	def SetRotation(self, angle):

		self.ReplaceSprite(self._spriteName, loop = False, dimensions = None, rotation = angle)

	# Movement management.

	def SetMovementVector(self, movementVector):

		self._movementVector = movementVector

	def EnableMovement(self, enable = True):

		self._movementStopped = not enable
		if self._movement:
			self._movement.Enable(enable)

	# Other operations.

	def Terminate(self):

		self._terminated = True

		self.OnTermination()

	# Callbacks.

	def OnCollision(self, node): pass
	def OnTermination(self): pass

	# Updating and rendering.

	def Update(self, milisecondsPassed):

		if IsOutsideScreen(self._position, self._dimensions):
			self.Terminate()
			return

		self._sprite.Update(milisecondsPassed)
		self.UpdateTimers(milisecondsPassed)

		if self._movement and self._movement.IsEnabled():

			self._movement.Update(milisecondsPassed)

			currentPosition = self._movement.GetCurrentPosition()
			self.SetPosition(currentPosition)

			currentRotation = self._movement.GetCurrentRotation()
			if currentRotation:
				self.ReplaceSprite(self._spriteName, rotation = currentRotation)

		if self._movementVector and not self._movementStopped:
			self._position += self._movementVector * milisecondsPassed

	def Render(self):

		self._sprite.Blit(GetScreen(), self._position)