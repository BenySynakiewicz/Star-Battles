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
from Engine.World.Utilities.Positioning import AtSameCenter

##
#
# The main class.
#
##

class AbsorptionEffect(Node):

	def __init__(self, scene, parentNode):

		super().__init__(scene, "Absorption", -2)

		self._sprite.SetLooping(False)

		self._parentNode = parentNode

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		self.SetRelativePosition(self._parentNode, AtSameCenter)

		if self._sprite.IsFinished():
			self.Terminate()