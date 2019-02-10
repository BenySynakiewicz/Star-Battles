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
from Engine.World.Concepts.Node import Node
from Engine.World.Nodes.Other.Effect import Effect
from Engine.World.Nodes.Weapons.Bomb import Bomb
from Engine.World.Nodes.Weapons.BulletFromPlayer import BulletFromPlayer
from Engine.World.Utilities.Positioning import AtSameCenter, AtTop, AtBottom
from Engine.Utilities.Color import Color
from Engine.Utilities.Direction import Direction
from Engine.Utilities.General import GetScreen, GetScreenDimensions
from Engine.Utilities.GUI import DrawBar
from Engine.Utilities.Vector import Vector

from numpy import clip

##
#
# Globals.
#
##

MaximumHealth = 100

##
#
# The main class.
#
##

class Player(Node):

	# The constructor.

	def __init__(self, scene):

		# Initialize the node.

		super().__init__(scene, "Player", zIndex = 1)

		self._collisionClasses = {"Participants", "Bonuses"}
		self._collisionExceptions = {"BulletFromPlayer"}

		# Initialize new member variables.

		self._health = MaximumHealth

		self._bulletEnergy = 100
		self._bombEnergy = 100
		self._shieldEnergy = 100

		self.__bombs = []

		self._shieldUp = False

	# Accessors.

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

		if State().GetBonusManager().IsTripleShotEnabled():
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

			if self._bombEnergy < 100:
				return

			if not State().GetBonusManager().IsTwoBombsEnabled():

				bomb = self._ShootSomething("Bomb")
				self.__bombs.append(bomb)

			else:

				leftBomb = self._ShootSomething("Bomb", +15)
				self.__bombs.append(leftBomb)

				rightBomb = self._ShootSomething("Bomb", -15)
				self.__bombs.append(rightBomb)

			self.ChangeBombEnergy(-100)

		else:

			for bomb in self.__bombs:
				bomb.Explode()

	# Updating and rendering.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		shieldEnergyChange = Parameters.ShieldEnergyRegeneration
		if self._shieldUp:
			shieldEnergyChange -= Parameters.ShieldEnergyUsage if not State().GetBonusManager().IsQuickerShieldEnabled() else Parameters.LowerShieldEnergyUsage

		self.ChangeBulletEnergy(milisecondsPassed * Parameters.BulletEnergyRegeneration)
		self.ChangeBombEnergy(milisecondsPassed * Parameters.BombEnergyRegeneration)
		self.ChangeShieldEnergy(milisecondsPassed * shieldEnergyChange)

		if not self._shieldEnergy:
			self._shieldUp = False

		self.__bombs[:] = filter(lambda x: not x.IsTerminated(), self.__bombs)

	def Render(self):

		super().Render()

		if self._shieldUp:

			# Render the shield.

			sprite = Resources().GetSprite("Shield")
			dimensions = sprite.GetDimensions()

			sprite.Blit(0, GetScreen(), AtSameCenter(self.GetPosition(), self.GetDimensions(), dimensions))

		# Render the health bar.

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

		# The shield is inpenetrable. Skip any collisions if the thing's up.

		if self._shieldUp:

			Resources().GetSound("Shield").Play()

			return

		# Absorp dropped items.

		nodeName = node.GetName()

		longTimeBonuses = {
			"TripleShotBonus"   : State().GetBonusManager().EnableTripleShot,
			"TwoBombsBonus"     : State().GetBonusManager().EnableTwoBombs,
			"QuickerShieldBonus": State().GetBonusManager().EnableQuickerShield,
		}

		oneTimeBonuses = {
			"ShootAroundBonus": Player.ShootAround,
		}

		if nodeName in longTimeBonuses or nodeName in oneTimeBonuses:

			if nodeName in longTimeBonuses: longTimeBonuses[nodeName]()
			else: oneTimeBonuses[nodeName](self)

			self._scene.UpdateBonusDescriptionText()

			# Create and show the visual effect and play the sound.

			self._scene.Append(Effect(self._scene, "Absorption", self, follow = True, zIndex = -1))
			Resources().GetSound("Absorption").Play()

			return

		# If the colliding node is not absorbable - destroy the Player.

		# self.Terminate()

		self._health = max(0, self._health - 5)

		if not self._health:
			self.Terminate()

	def OnTermination(self):

		Resources().GetSound("Destruction").Play()

	# Utilities.

	def _ShootSomething(self, somethingsName, angle = None):

		node = globals()[somethingsName](self._scene)
		node.SetRelativePosition(self, AtTop)

		if angle:

			node.SetPosition(node.GetPosition().GetRotatedAround(self.GetCenter(), angle))

			movementVector = (node.GetCenter() - self.GetCenter()).GetNormalized() * Parameters.BulletSpeed
			node.SetMovementVector(movementVector)

			node.SetRotation(angle)

		self._scene.Append(node)

		return node