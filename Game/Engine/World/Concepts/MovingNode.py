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

from Engine.World.Concepts.Node import Node

##
#
# The main class.
#
##

class MovingNode(Node):

	def __init__(self, scene, sprite, movementVector):

		super().__init__(scene, sprite)

		self._movementVector = movementVector
		self._stopped = False

	def GetMovementVector(self):

		return self._movementVector

	def SetMovementVector(self, movementVector):

		self._movementVector = movementVector

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if not self._stopped:
			self._position += self._movementVector * milisecondsPassed

	def StartMoving(self):

		self._stopped = False

	def StopMoving(self):

		self._stopped = True