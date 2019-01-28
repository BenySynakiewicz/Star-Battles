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

from Engine.Utilities.Direction import Direction
from Engine.World.Concepts.Entity import Entity

##
#
# The main class.
#
##

class MovingEntity(Entity):

	def __init__(self, scene, sprite, direction, speed):

		super().__init__(scene, sprite)

		self._direction = direction
		self._speed = speed
		self._stopped = False

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if not self._stopped:

			distance = milisecondsPassed * self._speed

			if   self._direction == Direction.Left  : self._position.X -= distance
			elif self._direction == Direction.Top   : self._position.Y -= distance
			elif self._direction == Direction.Right : self._position.X += distance
			elif self._direction == Direction.Bottom: self._position.Y += distance

	def StartMoving(self):

		self._stopped = False

	def StopMoving(self):

		self._stopped = True