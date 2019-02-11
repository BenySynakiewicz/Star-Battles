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
from Engine.Core.State import State
from Engine.Logic.BonusManager import BonusManager
from Engine.Utilities.Direction import Direction
from Engine.Utilities.General import GetScreen, GetScreenDimensions
from Engine.World.Nodes.Other.Effect import Effect
from Engine.World.Nodes.AbstractParticipant import AbstractParticipant
from Engine.World.Utilities.Positioners import AtSameCenter

from numpy import clip

##
#
# The main class.
#
##

class Player(AbstractParticipant):

	# The constructor.

	def __init__(self, scene):

		# Initialize the node.

		super().__init__(scene, "Player", 100, dropsBonus = True)

		self._collisionClasses = {"Participants", "Bonuses"}
		self._collisionExceptions = {"BulletFromPlayer"}

		# Initialize new member variables.

		self._bonusManager = BonusManager()

		self._bulletEnergy = 100
		self._bombEnergy = 100
		self._shieldEnergy = 100

		self._bombs = []

		self._shieldUp = False

	# Accessors.

	def GetBonusManager(self): return self._bonusManager
	def GetBulletEnergy(self): return self._bulletEnergy
	def GetBombEnergy(self): return self._bombEnergy
	def GetShieldEnergy(self): return self._shieldEnergy
	def IsShieldUp(self): return self._shieldUp

	# Basic operations.

	def ChangeBulletEnergy(self, change): self._bulletEnergy = clip(self._bulletEnergy + change, 0, 100)
	def ChangeBombEnergy(self, change): self._bombEnergy = clip(self._bombEnergy + change, 0, 100)
	def ChangeShieldEnergy(self, change): self._shieldEnergy = clip(self._shieldEnergy + change, 0, 100)

	# Movement.

	def Move(self, direction, amount = Parameters.PlayerSpeed):

		self._position.X = clip(

			self._position.X + (+amount if Direction.Right == direction else -amount),
			Parameters.Margin,
			GetScreenDimensions().X - Parameters.Margin - self._dimensions.X

		)

	# Using weapons.

	def Shoot(self):

		if self._bulletEnergy < 100:
			return

		self._ShootSomething("BulletFromPlayer")

		if self._bonusManager.IsTripleShotEnabled():
			self._ShootSomething("BulletFromPlayer", +10)
			self._ShootSomething("BulletFromPlayer", -10)

		self.ChangeBulletEnergy(-100)

	def ShootAround(self):

		numberOfBullets = 50
		radialStep = (360 / numberOfBullets)

		for n in range(numberOfBullets):
			self._ShootSomething("BulletFromPlayer", radialStep * n)

	def ShootBomb(self):

		if not self._bombs:

			if self._bombEnergy < 100:
				return

			if not self._bonusManager.IsTwoBombsEnabled():

				bomb = self._ShootSomething("Bomb")
				self._bombs.append(bomb)

			else:

				leftBomb = self._ShootSomething("Bomb", +15)
				self._bombs.append(leftBomb)

				rightBomb = self._ShootSomething("Bomb", -15)
				self._bombs.append(rightBomb)

			self.ChangeBombEnergy(-100)

		else:

			for bomb in self._bombs:
				bomb.Explode()

	# Updating and rendering.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		self._bonusManager.Update(milisecondsPassed)

		shieldEnergyChange = Parameters.ShieldEnergyRegeneration
		if self._shieldUp:
			shieldEnergyChange -= Parameters.ShieldEnergyUsage if not self._bonusManager.IsQuickerShieldEnabled() else Parameters.LowerShieldEnergyUsage

		self.ChangeBulletEnergy(milisecondsPassed * Parameters.BulletEnergyRegeneration)
		self.ChangeBombEnergy(milisecondsPassed * Parameters.BombEnergyRegeneration)
		self.ChangeShieldEnergy(milisecondsPassed * shieldEnergyChange)

		if not self._shieldEnergy:
			self._shieldUp = False

		self._bombs[:] = filter(lambda x: not x.IsTerminated(), self._bombs)

	def Render(self):

		super().Render()

		if self._shieldUp:

			# Render the shield.

			sprite = Resources().GetSprite("Shield")
			dimensions = sprite.GetDimensions()

			sprite.Blit(0, GetScreen(), AtSameCenter(self.GetPosition(), self.GetDimensions(), dimensions))

		# Render the health bar.

		self._RenderHealthBar()

	# Callbacks.

	def OnCollision(self, node):

		# The shield is inpenetrable. Skip any collisions if the thing's up.

		if self._shieldUp:

			Resources().GetSound("Shield").Play()

			return

		# Absorp dropped items.

		nodeName = node.GetName()

		bonuses = {
			"TripleShotBonus": self._bonusManager.EnableTripleShot,
			"TwoBombsBonus": self._bonusManager.EnableTwoBombs,
			"QuickerShieldBonus": self._bonusManager.EnableQuickerShield,
			"ShootAroundBonus": self.ShootAround,
		}

		if nodeName in bonuses:

			bonuses[nodeName]()

			self._scene.UpdateBonusDescriptionText()

			# Create and show the visual effect and play the sound.

			self._scene.Append(Effect(self._scene, "Absorption", self, follow = True, zIndex = -1))
			Resources().GetSound("Absorption").Play()

			return

		# If the colliding node is not absorbable - harm the player.

		self._OnUnprotectedCollision(node)