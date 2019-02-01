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
from Engine.World.Concepts.Node import Node
from Engine.World.Nodes.Bomb import Bomb
from Engine.World.Nodes.BulletFromPlayer import BulletFromPlayer
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

class Player(Node):

	def __init__(self, scene):

		super().__init__(scene, "Player", 1)

		self.SetCollisions({"Participants", "Bonuses"}, {"BulletFromPlayer"})

		self.Energy = SimpleNamespace(
			Bullet = 0,
			Bomb = 0,
			Shield = 0,
		)

		self._bonuses = SimpleNamespace(
			TripleShot = False,
			TwoBombs = False,
			QuickerShield = False,
		)

		self.__bombs = []
		self.ShieldIsUp = False

	def EnableTripleShotBonus(self):

		self._bonuses.TripleShot = True
		self._bonuses.TwoBombs = False
		self._bonuses.QuickerShield = False

	def EnableTwoBombsBonus(self):

		self._bonuses.TripleShot = False
		self._bonuses.TwoBombs = True
		self._bonuses.QuickerShield = False

	def EnableQuickerShieldBonus(self):

		self._bonuses.TripleShot = False
		self._bonuses.TwoBombs = False
		self._bonuses.QuickerShield = True

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

			bullet = BulletFromPlayer(self._scene)
			bullet.SetRelativePosition(self, AtTop)

			self._scene.AppendNode(bullet)

		else:

			centerBullet = BulletFromPlayer(self._scene)
			centerBullet.SetRelativePosition(self, AtTop)

			leftBullet = BulletFromPlayer(self._scene)
			leftBullet.SetPosition(centerBullet.GetPosition())
			leftBullet._position.X -= Parameters.MediumMargin + leftBullet.GetDimensions().X
			leftBullet.SetMovementVector(leftBullet.GetMovementVector() + Vector(-Parameters.SmallTrajectoryDeviation, 0))
			leftBullet.SetRotationToMovementVector()

			rightBullet = BulletFromPlayer(self._scene)
			rightBullet.SetPosition(centerBullet.GetPosition())
			rightBullet._position.X += centerBullet.GetDimensions().X + Parameters.MediumMargin
			rightBullet.SetMovementVector(rightBullet.GetMovementVector() + Vector(+Parameters.SmallTrajectoryDeviation, 0))
			rightBullet.SetRotationToMovementVector()

			self._scene.AppendNode(centerBullet)
			self._scene.AppendNode(leftBullet)
			self._scene.AppendNode(rightBullet)

		self.ChangeBulletEnergy(-100)

	def ShootBomb(self):

		if not self.__bombs:

			if self.Energy.Bomb < 100:
				return

			if not self._bonuses.TwoBombs:

				bomb = Bomb(self._scene)
				bomb.SetRelativePosition(self, AtTop)

				self.__bombs.append(bomb)
				self._scene.AppendNode(bomb)

			else:

				leftBomb = Bomb(self._scene)
				leftBomb.SetRelativePosition(self, AtTop)
				leftBomb._position.X -= leftBomb.GetDimensions().X
				leftBomb.SetMovementVector(Vector(-Parameters.BigTrajectoryDeviation, -Parameters.BombSpeed))
				leftBomb.SetRotationToMovementVector()

				rightBomb = Bomb(self._scene)
				rightBomb.SetRelativePosition(self, AtTop)
				rightBomb._position.X += rightBomb.GetDimensions().X
				rightBomb.SetMovementVector(Vector(+Parameters.BigTrajectoryDeviation, -Parameters.BombSpeed))
				rightBomb.SetRotationToMovementVector()

				self.__bombs.append(leftBomb)
				self.__bombs.append(rightBomb)

				self._scene.AppendNode(leftBomb)
				self._scene.AppendNode(rightBomb)

			self.ChangeBombEnergy(-100)

		else:

			for bomb in self.__bombs:
				bomb.Explode()

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		self.ChangeBulletEnergy(milisecondsPassed * Parameters.BulletEnergyRegeneration)
		self.ChangeBombEnergy(milisecondsPassed * Parameters.BombEnergyRegeneration)
		self.ChangeShieldEnergy(-(milisecondsPassed * (Parameters.ShieldEnergyUsage if not self._bonuses.QuickerShield else Parameters.LowerShieldEnergyUsage)) if self.ShieldIsUp else (milisecondsPassed * Parameters.ShieldEnergyRegeneration))

		if not self.Energy.Shield:
			self.ShieldIsUp = False

		self.__bombs[:] = filter(lambda x: not x._terminated, self.__bombs)

	def Render(self):

		super().Render()

		if self.ShieldIsUp:
			Resources().GetSprite("Shield").Blit(0, GetScreen(), self._position - Vector(15, 15))

	def OnCollision(self, node):

		if "TripleShotBonus" == type(node).__name__:
			self.EnableTripleShotBonus()
			return
		elif "TwoBombsBonus" == type(node).__name__:
			self.EnableTwoBombsBonus()
			return
		elif "QuickerShieldBonus" == type(node).__name__:
			self.EnableQuickerShieldBonus()
			return
		elif "Cargo" == type(node).__name__:
			return

		if not self.ShieldIsUp:
			Resources().GetSound("Destruction").Play()
			self.Terminate()
		else:
			Resources().GetSound("Shield").Play()