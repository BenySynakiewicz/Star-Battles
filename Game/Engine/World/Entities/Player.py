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
from Engine.World.Concepts.Entity import Entity
from Engine.World.Entities.Bomb import Bomb
from Engine.World.Entities.Bullet import Bullet
from Engine.World.Utilities.Positioning import AtTop
from Engine.Utilities.Direction import Direction
from Engine.Utilities.Vector import Vector
from Engine.Utilities.General import GetScreen, GetScreenDimensions

from copy import copy
from types import SimpleNamespace

from numpy import clip
import pygame

##
#
# The main class.
#
##

class Player(Entity):

	def __init__(self, scene):

		super().__init__(scene, "Player")

		self.Energy = SimpleNamespace(
			Bullet = 0,
			Bomb = 0,
			Shield = 0,
		)

		self._bonuses = SimpleNamespace(
			TripleShot = False,
		)

		self.__bombs = []
		self.ShieldIsUp = False

	def EnableTripleShotBonus(self):

		self._bonuses.TripleShot = True

	def ChangeBulletEnergy(self, change):

		self.Energy.Bullet = clip(self.Energy.Bullet + change, 0, 100)

	def ChangeBombEnergy(self, change):

		self.Energy.Bomb = clip(self.Energy.Bomb + change, 0, 100)

	def ChangeShieldEnergy(self, change):

		self.Energy.Shield = clip(self.Energy.Shield + change, 0, 100)

	def Move(self, direction):

		self._position.X = clip(

			self._position.X + (+8 if Direction.Right == direction else -8),
			Parameters.Margin,
			GetScreenDimensions().X - Parameters.Margin - self._dimensions.X

		)

	def Shoot(self):

		if self.Energy.Bullet < 100:
			return

		if not self._bonuses.TripleShot:

			bullet = Bullet(self._scene, "Player", Direction.Top)
			bullet.SetRelativePosition(self, AtTop)

			self._scene.AppendEntity(bullet)

		else:

			centerBullet = Bullet(self._scene, "Player", Direction.Top)
			centerBullet.SetRelativePosition(self, AtTop)

			leftBullet = Bullet(self._scene, "Player", Direction.Top)
			leftBullet.SetPosition(centerBullet.GetPosition())
			leftBullet._position.X -= Parameters.MediumMargin + leftBullet.GetDimensions().X

			rightBullet = Bullet(self._scene, "Player", Direction.Top)
			rightBullet.SetPosition(centerBullet.GetPosition())
			rightBullet._position.X += centerBullet.GetDimensions().X + Parameters.MediumMargin

			self._scene.AppendEntity(centerBullet)
			self._scene.AppendEntity(leftBullet)
			self._scene.AppendEntity(rightBullet)

		self.ChangeBulletEnergy(-100)

	def ShootBomb(self):

		if not self.__bombs:

			if self.Energy.Bomb < 100:
				return

			bomb = Bomb(self._scene)
			bomb.SetRelativePosition(self, AtTop)

			self.__bombs.append(bomb)
			self._scene.AppendEntity(bomb)

			self.ChangeBombEnergy(-100)

		else:

			for bomb in self.__bombs:
				bomb.Explode()

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		self.ChangeBulletEnergy(milisecondsPassed * Parameters.BulletEnergyRegeneration)
		self.ChangeBombEnergy(milisecondsPassed * Parameters.BombEnergyRegeneration)
		self.ChangeShieldEnergy(-(milisecondsPassed * Parameters.ShieldEnergyUsage) if self.ShieldIsUp else (milisecondsPassed * Parameters.ShieldEnergyRegeneration))

		if not self.Energy.Shield:
			self.ShieldIsUp = False

		self.__bombs[:] = filter(lambda x: not x._terminated, self.__bombs)

	def Render(self):

		super().Render()

		if self.ShieldIsUp:
			Resources().GetSprite("Shield").Blit(GetScreen(), self._position - Vector(15, 15))

	def OnCollision(self, entity):

		if "TripleShotBonus" == type(entity).__name__:
			return

		if not self.ShieldIsUp:
			Resources().GetSound("Destruction").Play()
			self._terminated = True
		else:
			Resources().GetSound("Shield").Play()