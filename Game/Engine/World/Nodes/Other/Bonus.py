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
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Movement import Movement
from Engine.World.Concepts.Node import Node

##
#
# The main class.
#
##

class Bonus(Node):

	# The constructor.

	def __init__(self, scene, spriteIndex, name):

		# Initialize the node.

		super().__init__(scene, f"Bonus {spriteIndex}", zIndex = 2)

		self._movement = Movement(Parameters.BonusSpeed, Vector(0, 1))

		self._name = name
		self._collisionClasses = {"Bonuses"}

	# Callbacks.

	def OnCollision(self, node):

		if "Player" == node.GetName():
			self.Terminate()