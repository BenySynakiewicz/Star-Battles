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
from Engine.Utilities.Direction import Direction
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.MovingEntity import MovingEntity

##
#
# The main class.
#
##

class Bullet(MovingEntity):

	def __init__(self, scene, creator, direction):

		super().__init__(
			scene,
			"Bullet (Green)" if Direction.Top == direction else "Bullet (Red)",
			Vector(0, -Parameters.BulletSpeed) if Direction.Top == direction else Vector(0, +Parameters.BulletSpeed)
		)

		self._creator = creator

		Resources().GetSound("Bullet").Play()

	def GetCreator(self):

		return self._creator

	# Inherited methods.

	def OnCollision(self, entity):

		if "Enemy" == type(entity).__name__ and "Enemy" == self.GetCreator():
			return

		self.Terminate()