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
from Engine.World.Utilities.Positioners import AtSameCenter

##
#
# The main class.
#
##

class Effect(Node):

	# The constructor.

	def __init__(
		self,
		scene,
		spriteName,
		parentNode,
		follow = False,
		dimensions = None,
		collisionClasses = set(),
		zIndex = 3
	):

		# Initialize the node.

		super().__init__(scene, spriteName, dimensions = dimensions, zIndex = zIndex)

		self._collisionClasses = collisionClasses
		self._sprite.SetLooping(False)

		# Initialize new member variables.

		self._parentNode = parentNode
		self._followParent = follow

		if self._parentNode:
			self.SetRelativePosition(self._parentNode, AtSameCenter)

	# Updating.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._parentNode and self._followParent:
			self.SetRelativePosition(self._parentNode, AtSameCenter)

		if self._sprite.IsFinished():
			self.Terminate()