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
from Engine.Utilities.General import GetScreen, GetScreenDimensions
from Engine.Utilities.General import Decision
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.MovingNode import MovingNode
from Engine.World.Nodes.Bullet import Bullet
from Engine.World.Nodes.TripleShotBonus import TripleShotBonus
from Engine.World.Nodes.TwoBombsBonus import TwoBombsBonus
from Engine.World.Nodes.QuickerShieldBonus import QuickerShieldBonus
from Engine.World.Utilities.Positioning import AtBottom

import pygame

##
#
# The main class.
#
##

class Enemy(MovingNode):

	def __init__(self, scene, verticalOffset, row, direction):

		super().__init__(scene, "Enemy", Vector(+Parameters.EnemySpeed, 0) if Direction.Right == direction else Vector(-Parameters.EnemySpeed, 0), 1)

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

		bullet = Bullet(self._scene, "Enemy", Direction.Bottom)
		bullet.SetRelativePosition(self, AtBottom)
		bullet.ShotBy = "Enemy"

		self._scene.AppendNode(bullet)
		self.ClearTimer("Shot")

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._isDestroyed and self._sprite.IsFinished():
			self.Terminate()

		if not self._isDestroyed and Decision(self.GetTimer("Shot") / 200000):
			self.Shoot()

	def OnCollision(self, node):

		if "Bullet" == type(node).__name__ and "Enemy" == node.GetCreator():
			return

		self.Destroy()

	def OnTermination(self):

		if Decision(Parameters.TripleShotBonusProbability):

			bonus = TripleShotBonus(self._scene)
			bonus.SetRelativePosition(self, AtBottom)
	
			self._scene.AppendNode(bonus)

		elif Decision(Parameters.TwoBombsBonusProbability):

			bonus = TwoBombsBonus(self._scene)
			bonus.SetRelativePosition(self, AtBottom)
	
			self._scene.AppendNode(bonus)

		elif Decision(Parameters.QuickerShieldBonusProbability):

			bonus = QuickerShieldBonus(self._scene)
			bonus.SetRelativePosition(self, AtBottom)
	
			self._scene.AppendNode(bonus)