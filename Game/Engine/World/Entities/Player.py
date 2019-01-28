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

		self.Bomb = None
		self.ShieldIsUp = False

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

		bullet = Bullet(self._scene, "Player", Direction.Top)
		bullet._position = AtTop(self._position, self._dimensions, bullet._dimensions)

		self._scene.AppendEntity(bullet)
		self.ChangeBulletEnergy(-100)

	def ShootBomb(self):

		if not self.Bomb:

			if self.Energy.Bomb < 100 or self.Bomb:
				return

			self.Bomb = Bomb(self._scene)
			self.Bomb._position = AtTop(self._position, self._dimensions, self.Bomb._dimensions)

			self._scene.AppendEntity(self.Bomb)
			self.ChangeBombEnergy(-100)

		else:

			self.Bomb.Explode()

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		self.ChangeBulletEnergy(milisecondsPassed * Parameters.BulletEnergyRegeneration)
		self.ChangeBombEnergy(milisecondsPassed * Parameters.BombEnergyRegeneration)
		self.ChangeShieldEnergy(-(milisecondsPassed * Parameters.ShieldEnergyUsage) if self.ShieldIsUp else (milisecondsPassed * Parameters.ShieldEnergyRegeneration))

		if not self.Energy.Shield:
			self.ShieldIsUp = False

		if self.Bomb and self.Bomb._terminated:
			self.Bomb = None

	def Render(self):

		super().Render()

		if self.ShieldIsUp:
			Resources().GetSprite("Shield").Blit(GetScreen(), self._position - Vector(15, 15))

	def OnCollision(self, entity):

		if not self.ShieldIsUp:
			Resources().GetSound("Destruction").Play()
			self._terminated = True
		else:
			Resources().GetSound("Shield").Play()