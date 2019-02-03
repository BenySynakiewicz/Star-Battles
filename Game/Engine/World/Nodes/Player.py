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
from Engine.World.Nodes.Effects.AbsorptionEffect import AbsorptionEffect
from Engine.World.Nodes.Bomb import Bomb
from Engine.World.Nodes.BulletFromPlayer import BulletFromPlayer
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

		self._scene.UpdateBonusDescriptionText()

	def EnableTwoBombsBonus(self):

		self._bonuses.TripleShot = False
		self._bonuses.TwoBombs = True
		self._bonuses.QuickerShield = False

		self._scene.UpdateBonusDescriptionText()

	def EnableQuickerShieldBonus(self):

		self._bonuses.TripleShot = False
		self._bonuses.TwoBombs = False
		self._bonuses.QuickerShield = True

		self._scene.UpdateBonusDescriptionText()

	def EnableShootAroundBonus(self):

		self.ShootAround()

		self._scene.UpdateBonusDescriptionText()

	def ChangeBulletEnergy(self, change):

		self.Energy.Bullet = clip(self.Energy.Bullet + change, 0, 100)

	def ChangeBombEnergy(self, change):

		self.Energy.Bomb = clip(self.Energy.Bomb + change, 0, 100)

	def ChangeShieldEnergy(self, change):

		self.Energy.Shield = clip(self.Energy.Shield + change, 0, 100)

	def Move(self, direction):

		self._position.X = clip(

			self._position.X + (+Parameters.PlayerSpeed if Direction.Right == direction else -Parameters.PlayerSpeed),
			Parameters.Margin,
			GetScreenDimensions().X - Parameters.Margin - self._dimensions.X

		)

	def Shoot(self):

		if self.Energy.Bullet < 100:
			return

		self._ShootSomething("BulletFromPlayer")

		if self._bonuses.TripleShot:
			self._ShootSomething("BulletFromPlayer", +10)
			self._ShootSomething("BulletFromPlayer", -10)

		self.ChangeBulletEnergy(-100)

	def ShootAround(self):

		numberOfBullets = 50
		radialStep = (360 / numberOfBullets)

		for n in range(numberOfBullets):
			self._ShootSomething("BulletFromPlayer", radialStep * n)

	def ShootBomb(self):

		if not self.__bombs:

			if self.Energy.Bomb < 100:
				return

			if not self._bonuses.TwoBombs:

				bomb = self._ShootSomething("Bomb")
				self.__bombs.append(bomb)

			else:

				leftBomb = self._ShootSomething("Bomb", +10)
				self.__bombs.append(leftBomb)

				rightBomb = self._ShootSomething("Bomb", -10)
				self.__bombs.append(rightBomb)

			self.ChangeBombEnergy(-100)

		else:

			for bomb in self.__bombs:
				bomb.Explode()

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		shieldEnergyChange = Parameters.ShieldEnergyRegeneration
		if self.ShieldIsUp:
			shieldEnergyChange -= Parameters.ShieldEnergyUsage if not self._bonuses.QuickerShield else Parameters.LowerShieldEnergyUsage

		self.ChangeBulletEnergy(milisecondsPassed * Parameters.BulletEnergyRegeneration)
		self.ChangeBombEnergy(milisecondsPassed * Parameters.BombEnergyRegeneration)
		self.ChangeShieldEnergy(milisecondsPassed * shieldEnergyChange)

		if not self.Energy.Shield:
			self.ShieldIsUp = False

		self.__bombs[:] = filter(lambda x: not x._terminated, self.__bombs)

	def Render(self):

		super().Render()

		if self.ShieldIsUp:
			Resources().GetSprite("Shield").Blit(0, GetScreen(), self._position - Vector(15, 15))

	def OnCollision(self, node):

		# The shield is inpenetrable. Skip any collisions if the thing's up.

		if self.ShieldIsUp:

			Resources().GetSound("Shield").Play()

			return

		# Absorp dropped items.

		nodeName = type(node).__name__
		absorbableNodes = {
			"TripleShotBonus"   : Player.EnableTripleShotBonus,
			"TwoBombsBonus"     : Player.EnableTwoBombsBonus,
			"QuickerShieldBonus": Player.EnableQuickerShieldBonus,
			"ShootAroundBonus"  : Player.EnableShootAroundBonus,
		}

		if nodeName in absorbableNodes:

			absorbableNodes[nodeName](self)

			# Create and show the visual effect and play the sound.

			self._scene.AppendNode(AbsorptionEffect(self._scene, self))
			Resources().GetSound("Absorption").Play()

			return

		# If the colliding node is not absorbable - destroy the Player.

		Resources().GetSound("Destruction").Play()
		self.Terminate()

	# Private methods.

	def _ShootSomething(self, somethingsName, angle = None):

		node = globals()[somethingsName](self._scene)
		node.SetRelativePosition(self, AtTop)

		if angle:

			node.SetPosition(node.GetPosition().GetRotatedAround(self.GetCenter(), angle))

			movementVector = (node.GetCenter() - self.GetCenter()).GetNormalized() * Parameters.BulletSpeed
			node.SetMovementVector(movementVector)

			node.SetRotation(angle)

		self._scene.AppendNode(node)

		return node