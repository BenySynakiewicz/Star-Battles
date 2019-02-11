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
from Engine.Utilities.General import GetScreen
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Movement import Movement
from Engine.World.Concepts.Node import Node
from Engine.World.Nodes.Other.Effect import Effect
from Engine.World.Utilities.Positioners import AtSameCenter

##
#
# The main class.
#
##

class Bomb(Node):

	def __init__(self, scene):

		super().__init__(scene, "Bomb")#, movementVector = Vector(0, -Parameters.BombSpeed))

		self._collisionClasses = {"Participants"}
		self._collisionExceptions = {"Bomb"}

		self._movement = Movement(Parameters.BombSpeed, Vector(0, -1))

		Resources().GetSound("Bomb").Play()

	def Explode(self):

		self._scene.Append(Effect(self._scene, "Explosion", self, collisionClasses = {"Participants"}))

		self.Terminate()

	# Inherited methods.

	def Render(self):

		super().Render()

		smallShieldSprite = Resources().GetSprite("Shield", dimensions = Vector(80, 80))
		smallShieldSprite.Blit(
			0,
			GetScreen(),
			AtSameCenter(self.GetPosition(), self.GetDimensions(), smallShieldSprite.GetDimensions()),
		)

	def OnCollision(self, node):

		if "BulletFromEnemy" == type(node).__name__ or "BulletFromPlayer" == type(node).__name__:
			return

		if not self._terminated:
			self.Explode()