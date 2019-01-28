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
from Engine.World.Concepts.MovingEntity import MovingEntity
from Engine.World.Entities.Bullet import Bullet
from Engine.World.Entities.TripleShotBonus import TripleShotBonus
from Engine.World.Utilities.Positioning import AtBottom

import pygame

##
#
# The main class.
#
##

class Enemy(MovingEntity):

	def __init__(self, scene, verticalOffset, row, direction):

		super().__init__(scene, "Enemy", Vector(+Parameters.EnemySpeed, 0) if Direction.Right == direction else Vector(-Parameters.EnemySpeed, 0))

		self.Direction = direction

		self._position.X = -(self._dimensions.X - 1) if (Direction.Right == self.Direction) else (GetScreenDimensions().X - 1)
		self._position.Y = verticalOffset + row * (self._dimensions.Y + Parameters.Margin)

		self.AppendTimer("Shot")
		self.DestroyedByPlayer = False

	def Shoot(self):

		bullet = Bullet(self._scene, "Enemy", Direction.Bottom)
		bullet.SetRelativePosition(self, AtBottom)
		bullet.ShotBy = "Enemy"

		self._scene.AppendEntity(bullet)
		self.ClearTimer("Shot")

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if Decision(self.GetTimer("Shot") / 200000):
			self.Shoot()

	def Render(self):

		super().Render()

	def OnCollision(self, entity):

		if "Bullet" == type(entity).__name__ and "Enemy" == entity.GetCreator():
			return

		self.Terminate()
		self.DestroyedByPlayer = True

		Resources().GetSound("Destruction").Play()

	def OnTermination(self):

		if Decision(Parameters.TripleShotBonusProbability):

			bonus = TripleShotBonus(self._scene)
			bonus.SetRelativePosition(self, AtBottom)
	
			self._scene.AppendEntity(bonus)