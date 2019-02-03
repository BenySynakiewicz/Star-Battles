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
from Engine.World.Concepts.MovingNode import MovingNode
from Engine.World.Nodes.BulletFromEnemy import BulletFromEnemy
from Engine.World.Nodes.Cargo import Cargo
from Engine.World.Nodes.ShootAroundBonus import ShootAroundBonus
from Engine.World.Nodes.TripleShotBonus import TripleShotBonus
from Engine.World.Nodes.TwoBombsBonus import TwoBombsBonus
from Engine.World.Nodes.QuickerShieldBonus import QuickerShieldBonus
from Engine.World.Utilities.Positioning import AtBottom

##
#
# The main class.
#
##

class Enemy(MovingNode):

	def __init__(self, scene, verticalOffset, row, direction):

		super().__init__(scene, "Enemy", Vector(+Parameters.EnemySpeed if Direction.Right == direction else -Parameters.EnemySpeed, 0), 1)

		self.SetCollisions({"Participants"}, {"BulletFromEnemy"})

		self.Direction = direction

		self._position.X = -(self._dimensions.X - 1) if (Direction.Right == self.Direction) else (GetScreenDimensions().X - 1)
		self._position.Y = verticalOffset + row * (self._dimensions.Y + Parameters.Margin)

		self.AppendTimer("Shot")
		self.DestroyedByPlayer = False

		self._isDestroyed = False

	def Destroy(self):

		if self._isDestroyed:
			return

		self.ReplaceSprite("Small Explosion", False)
		Resources().GetSound("Destruction").Play()

		self.AppendTimer("Destruction")

		self.DestroyedByPlayer = True
		self._isDestroyed = True

	def Shoot(self):

		bullet = BulletFromEnemy(self._scene)
		bullet.SetRelativePosition(self, AtBottom)

		self._scene.AppendNode(bullet)
		self.ClearTimer("Shot")

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._isDestroyed and self._sprite.IsFinished():
			self.Terminate()

		if not self._isDestroyed and "Shoot" == GetDecision({"Shoot": self.GetTimer("Shot") / 200000}):
			self.Shoot()

	def OnCollision(self, node):

		self.Destroy()

	def OnTermination(self):

		possibilities = {
			"TripleShotBonus"   : Parameters.TripleShotBonusProbability,
			"TwoBombsBonus"     : Parameters.TwoBombsBonusProbability,
			"QuickerShieldBonus": Parameters.QuickerShieldBonusProbability,
			"ShootAroundBonus"  : Parameters.ShootAroundBonusProbability,
			"Cargo"             : Parameters.CargoProbability,
		}

		decision = GetDecision(possibilities)
		if not decision:
			return

		bonusNodeName = decision[0]

		bonusNode = globals()[bonusNodeName](self._scene)
		bonusNode.SetRelativePosition(self, AtBottom)

		self._scene.AppendNode(bonusNode)