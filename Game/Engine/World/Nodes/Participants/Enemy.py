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
from Engine.Utilities.General import GetDecision, GetScreenDimensions
from Engine.Utilities.Vector import Vector
from Engine.World.Nodes.AbstractParticipant import AbstractParticipant
from Engine.World.Utilities.Positioning import AtBottom

##
#
# Globals.
#
##

ExplosionDimensions = Vector(125, 125)
ShootingProbabilityDivisor = 200000

##
#
# The main class.
#
##

class Enemy(AbstractParticipant):

	# The constructor.

	def __init__(self, scene, verticalOffset, row, direction):

		# Initialize the node.

		super().__init__(scene, "Enemy", dropsBonus = True, movementVector = Vector(direction * Parameters.EnemySpeed, 0))

		self._collisionClasses = {"Participants"}
		self._collisionExceptions = {"BulletFromEnemy"}

		self._position.X = -(self._dimensions.X - 1) if Direction.Right == direction else (GetScreenDimensions().X - 1)
		self._position.Y = verticalOffset + row * (self._dimensions.Y + Parameters.Margin)

		# Initialize new member variables.

		self.AppendTimer("Shot")

	# Operations.

	def Destroy(self):

		if self._isDestroyed:
			return

		self.ReplaceSprite("Explosion", dimensions = ExplosionDimensions, loop = False)
		Resources().GetSound("Destruction").Play()

		self._isDestroyed = True

	# Weapons.

	def Shoot(self):

		self._ShootSomething("BulletFromEnemy", position = AtBottom)

		self.ClearTimer("Shot")

	# Updating.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._isDestroyed and self._sprite.IsFinished():
			self.Terminate()

		if not self._isDestroyed and "Shoot" == GetDecision({"Shoot": self.GetTimer("Shot") / ShootingProbabilityDivisor}):
			self.Shoot()