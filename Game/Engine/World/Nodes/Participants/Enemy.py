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
from Engine.Utilities.General import GetScreenDimensions
from Engine.Utilities.General import GetDecision
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Node import Node
from Engine.World.Nodes.Weapons.BulletFromEnemy import BulletFromEnemy
from Engine.World.Nodes.Other.Bonus import Bonus
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

class Enemy(Node):

	# The constructor.

	def __init__(self, scene, verticalOffset, row, direction):

		# Initialize the node.

		super().__init__(scene, "Enemy", movementVector = Vector(direction * Parameters.EnemySpeed, 0), zIndex = 1)

		self._collisionClasses = {"Participants"}
		self._collisionExceptions = {"BulletFromEnemy"}

		self._position.X = -(self._dimensions.X - 1) if Direction.Right == direction else (GetScreenDimensions().X - 1)
		self._position.Y = verticalOffset + row * (self._dimensions.Y + Parameters.Margin)

		# Initialize new member variables.

		self._isDestroyed = False

		self.AppendTimer("Shot")

	# Accessors.

	def IsDestroyedByPlayer(self): return self._isDestroyed

	# Operations.

	def Destroy(self):

		if self._isDestroyed:
			return

		self.ReplaceSprite("Explosion", dimensions = ExplosionDimensions, loop = False)
		Resources().GetSound("Destruction").Play()

		self._isDestroyed = True

	# Weapons.

	def Shoot(self):

		bullet = BulletFromEnemy(self._scene)
		bullet.SetRelativePosition(self, AtBottom)

		self._scene.Append(bullet)
		self.ClearTimer("Shot")

	# Updating.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._isDestroyed and self._sprite.IsFinished():
			self.Terminate()

		if not self._isDestroyed and "Shoot" == GetDecision({"Shoot": self.GetTimer("Shot") / ShootingProbabilityDivisor}):
			self.Shoot()

	# Callbacks.

	def OnCollision(self, node):

		self.Destroy()

	def OnTermination(self):

		possibilities = {
			"TripleShotBonus"   : Parameters.TripleShotBonusProbability,
			"TwoBombsBonus"     : Parameters.TwoBombsBonusProbability,
			"QuickerShieldBonus": Parameters.QuickerShieldBonusProbability,
			"ShootAroundBonus"  : Parameters.ShootAroundBonusProbability,
		}

		decision = GetDecision(possibilities)
		if not decision:
			return

		spriteIndices = {
			"TripleShotBonus"   : 1,
			"TwoBombsBonus"     : 2,
			"QuickerShieldBonus": 3,
			"ShootAroundBonus"  : 4,
		}

		bonusName = decision[0]

		bonusNode = Bonus(self._scene, spriteIndices[bonusName], bonusName)
		bonusNode.SetRelativePosition(self, AtBottom)

		self._scene.Append(bonusNode)