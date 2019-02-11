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
from Engine.Utilities.Color import Color, SetAlpha
from Engine.Utilities.General import GetDecision, GetScreen
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Node import Node
from Engine.World.Nodes.Other.Bonus import Bonus
from Engine.World.Utilities.Positioners import AtTop, AtBottom
from Engine.World.Nodes.Weapons.Bomb import Bomb
from Engine.World.Nodes.Weapons.BulletFromEnemy import BulletFromEnemy
from Engine.World.Nodes.Weapons.BulletFromPlayer import BulletFromPlayer
from Engine.World.Widgets.Bar import Bar

##
#
# Globals.
#
##

HealthBarAlpha = 50

##
#
# The main class.
#
##

class AbstractParticipant(Node):

	# The constructor.

	def __init__(self, scene, sprite, health = 1, dropsBonus = True):

		# Initialize the node.

		super().__init__(scene, sprite, zIndex = 1)

		# Initialize new member variables.

		self._maximumHealth = health
		self._currentHealth = self._maximumHealth

		self._dropsBonus = dropsBonus
		self._isDestroyed = False

		self._healthBar = Bar(
			self._scene,
			SetAlpha(Color.Red, HealthBarAlpha),
			SetAlpha(Color.Green, HealthBarAlpha),
			Vector(self._dimensions.X, Parameters.HealthBarHeight),
			interpolateColors = True,
			rounded = True,
		)

	# Accessors.

	def IsDestroyed(self): return self._isDestroyed

	# Operations.

	def Destroy(self):

		self._isDestroyed = True

		self.Terminate()

	# Callbacks.

	def OnCollision(self, node):

		self._OnUnprotectedCollision(node)

	def OnDestruction(self):

		Resources().GetSound("Destruction").Play()

		self._isDestroyed = True

	def OnTermination(self):

		if self._dropsBonus:
			self._DropBonus()

	# Utilities.

	def _OnUnprotectedCollision(self, node):

		self._currentHealth = max(0, self._currentHealth - 5)

		if not self._currentHealth:
			self.Destroy()

	def _DropBonus(self):

		possibilities = {
			"TripleShotBonus": Parameters.TripleShotBonusProbability,
			"TwoBombsBonus": Parameters.TwoBombsBonusProbability,
			"QuickerShieldBonus": Parameters.QuickerShieldBonusProbability,
			"ShootAroundBonus": Parameters.ShootAroundBonusProbability,
			"HealthBonus": Parameters.HealthBonusProbability,
		}

		decision = GetDecision(possibilities)
		if not decision:
			return

		spriteIndices = {
			"TripleShotBonus": 1,
			"TwoBombsBonus": 2,
			"QuickerShieldBonus": 3,
			"ShootAroundBonus": 4,
			"HealthBonus": 5,
		}

		bonusName = decision[0]

		bonusNode = Bonus(self._scene, spriteIndices[bonusName], bonusName)
		bonusNode.SetRelativePosition(self, AtBottom)

		self._scene.Append(bonusNode)

	def _RenderHealthBar(self):

		dimensions = self._healthBar.GetDimensions()
		position = self._position - (0, dimensions.Y + 4 * Parameters.SmallMargin) + ((self._dimensions - dimensions).X / 2, 0)

		self._healthBar.SetProgress((self._currentHealth / self._maximumHealth) * 100)
		self._healthBar.SetPosition(position)
		self._healthBar.Render()

	def _ShootSomething(self, name, angle = None, position = AtTop, additionalRotation = 0):

		node = globals()[name](self._scene)
		node.SetRelativePosition(self, position)

		if angle:

			node.SetPosition(node.GetPosition().GetRotatedAround(self.GetCenter(), angle))

			movementVector = node.GetCenter() - self.GetCenter()
			node.GetMovement().Set(Parameters.BulletSpeed, movementVector)

			node.SetRotation(angle + additionalRotation)

		self._scene.Append(node)

		return node