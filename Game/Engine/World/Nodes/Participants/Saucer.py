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
from Engine.Utilities.Color import Color
from Engine.Utilities.Direction import Direction
from Engine.Utilities.General import GetScreenDimensions
from Engine.Utilities.General import GetDecision, GetScreen
from Engine.Utilities.Vector import Vector
from Engine.Utilities.GUI import DrawBar
from Engine.World.Concepts.Node import Node
from Engine.World.Nodes.Other.Bonus import Bonus
from Engine.World.Nodes.Weapons.BulletFromEnemy import BulletFromEnemy
from Engine.World.Utilities.Positioning import AtBottom

##
#
# Globals.
#
##

ExplosionDimensions = Vector(200, 200)
ShootingProbabilityDivisor = 200000

MaximumHealth = 500

##
#
# The main class.
#
##

class Saucer(Node):

	# The constructor.

	def __init__(self, scene, verticalOffset, row, direction):

		# Initialize the node.

		super().__init__(scene, "Saucer", movementVector = Vector(direction * Parameters.EnemySpeed, 0), zIndex = 1)

		self._collisionClasses = {"Participants"}
		self._collisionExceptions = {"BulletFromEnemy"}

		self._position.X = -(self._dimensions.X - 1) if Direction.Right == direction else (GetScreenDimensions().X - 1)
		self._position.Y = verticalOffset + row * (self._dimensions.Y + Parameters.Margin)

		# Initialize new member variables.

		self._health = MaximumHealth
		self._isDestroyed = False

		self.AppendTimer("Shot")
		self.DestroyedByPlayer = False

	# Accessors.

	def IsDestroyedByPlayer(self): return self._isDestroyed

	# Operations.

	def Destroy(self):

		if self._isDestroyed:
			return

		self.ReplaceSprite("Explosion", dimensions = ExplosionDimensions, loop = False)
		Resources().GetSound("Destruction").Play()

		self._isDestroyed = True

	# Using weapons.

	def Shoot(self):

		self._ShootSomething("BulletFromEnemy")

		self.ClearTimer("Shot")

	# Updating and rendering.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._isDestroyed and self._sprite.IsFinished():
			self.Terminate()

		if not self._isDestroyed and "Shoot" == GetDecision({"Shoot": self.GetTimer("Shot") / ShootingProbabilityDivisor}):
			self.Shoot()

	def Render(self):

		super().Render()

		if not self._isDestroyed:

			barDimensions = Vector(self.GetDimensions().X, Parameters.HealthBarHeight)
			DrawBar(

				GetScreen(),

				self._position - (0, barDimensions.Y + Parameters.SmallMargin) + ((self._dimensions.X - barDimensions.X) / 2, 0),
				barDimensions,

				Color.Red,
				(self._health / MaximumHealth) * 100,

			)

	# Callbacks.

	def OnCollision(self, node):

		self._health = max(0, self._health - 5)

		if not self._health:
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

	# Utilities.

	def _ShootSomething(self, somethingsName, angle = None):

		node = globals()[somethingsName](self._scene)
		node.SetRelativePosition(self, AtBottom)

		if angle:

			node.SetPosition(node.GetPosition().GetRotatedAround(self.GetCenter(), angle))

			movementVector = (self.GetCenter() - node.GetCenter()).GetNormalized() * Parameters.BulletSpeed
			node.SetMovementVector(movementVector)

			node.SetRotation(angle)

		self._scene.Append(node)

		return node