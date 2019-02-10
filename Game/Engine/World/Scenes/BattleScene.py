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
from Engine.Logic.BattleManager import BattleManager
from Engine.Media.Utilities.SurfaceProcessor import Desaturate
from Engine.World.Concepts.Scene import Scene
from Engine.World.Nodes.Participants.Player import Player
from Engine.World.Nodes.Participants.Enemy import Enemy
from Engine.World.Scenes.EndGameScene import EndGameScene
from Engine.Utilities.Direction import Direction
from Engine.Utilities.Vector import Vector
from Engine.Utilities.Color import Color
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, GetScreenDimensions, RenderText
from Engine.Utilities.GUI import DrawBar

from pygame import (
	mouse,
	KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE,
	MOUSEBUTTONDOWN,
)

##
#
# The main class.
#
##

class BattleScene(Scene):

	def __init__(self):

		super().__init__("Background")

		# Initialize texts.

		self._scoreText = None
		self._bonusDescriptionText = None

		self.UpdateScoreText()

		# Initialize the player.

		self.Player = Player(self)

		screenDimensions = GetScreenDimensions()
		topRightCornerPosition = screenDimensions - self.Player.GetDimensions()

		self.Player._position = Vector(

			topRightCornerPosition.X / 2,
			topRightCornerPosition.Y - 2 * Parameters.Margin - Parameters.BarHeight,

		)

		self.Append(self.Player)

		# Initialize the battle manager.

		self._battleManager = BattleManager(self, 2 * Parameters.Margin + GetDimensions(self._scoreText).Y)

	def Show(self):

		mouse.set_visible(False)

	def UpdateScoreText(self):

		self._scoreText = RenderText(f"{State().GetScoreManager().GetCurrentScore()} points", Resources().GetFont("Exo 2", Parameters.SmallTextHeight))

	def UpdateBonusDescriptionText(self):

		if State().GetBonusManager().IsTripleShotEnabled():
			description = "TRIPLE SHOT bonus is now active"
		elif State().GetBonusManager().IsTwoBombsEnabled():
			description = "TWO BOMBS bonus is now active"
		elif State().GetBonusManager().IsQuickerShieldEnabled():
			description = "QUICKER SHIELD bonus is now active"
		else:
			description = None

		self._bonusDescriptionText = RenderText(description, Resources().GetFont("Exo 2", Parameters.SmallTextHeight)) if description else None

	def React(self, events, keys):

		# Process events.

		for event in events:

			if KEYDOWN == event.type:

				if K_UP == event.key:
					self.Player.Shoot()

				elif K_SPACE == event.key:
					self.Player.ShootBomb()

			elif MOUSEBUTTONDOWN == event.type:

				leftButton, middleButton, rightButton = mouse.get_pressed()

				if leftButton:
					self.Player.Shoot()

				elif middleButton:
					self.Player.ShootBomb()

		# Process pressed keys.

		if keys[K_LEFT]:
			self.Player.Move(Direction.Left)

		elif keys[K_RIGHT]:
			self.Player.Move(Direction.Right)

		rightMouseButton = mouse.get_pressed()[2]
		self.Player._shieldUp = bool(keys[K_DOWN] or rightMouseButton)

		# Process mouse input.

		mouseMovement = mouse.get_rel()
		self.Player.Move(Direction.Right, mouseMovement[0])

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		# Finish the game if the player has been destroyed.

		if self.Player._terminated:
			Resources()._backgrounds["Screenshot"] = Desaturate(GetScreen())
			self._nextScene = EndGameScene()
			return

		# Remove terminated nodes (and update the score).

		for node in self._nodes:

			if node._terminated and "Enemy" == type(node).__name__ and node.IsDestroyedByPlayer():
				State().GetScoreManager().Update(+Parameters.EnemyValue)
				self.UpdateScoreText()

		self._nodes[:] = filter(lambda node: not node._terminated, self._nodes)

		# Update the battle manager.

		self._battleManager.Update(milisecondsPassed)

		# Find collisions.

		allFoundCollisions = {}

		for node in self._nodes:

			collisions = []

			for alreadyProcessedNode, alreadyProcessedCollisions in allFoundCollisions.items():
				if node in alreadyProcessedCollisions:
					collisions.append(alreadyProcessedNode)

			newCollisions = [x for x in self._nodes if x not in collisions and node.DoesCollideWith(x)]
			collisions.extend(newCollisions)

			if collisions:
				allFoundCollisions[node] = collisions

		for node, collidingNodes in allFoundCollisions.items():

			for collidingNode in collidingNodes:

				node.OnCollision(collidingNode)
				collidingNode.OnCollision(node)

	def Render(self):

		# Render the background.

		super().Render()

		# Retrieve some parameters.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Draw the score.

		Blit(screen, self._scoreText, Vector(Parameters.Margin, Parameters.Margin))

		if self._bonusDescriptionText:
			Blit(screen, self._bonusDescriptionText, Vector(screenDimensions.X - Parameters.Margin - GetDimensions(self._bonusDescriptionText).X, Parameters.Margin))

		# Calculate the bar dimensions.

		barDimensions = Vector(screenDimensions.X / 3, Parameters.BarHeight)
		barVerticalPosition = screenDimensions.Y - barDimensions.Y

		# Draw the bullet energy bar.

		DrawBar(

			screen,

			Vector(0 * barDimensions.X, barVerticalPosition),
			barDimensions,

			Color.Green if (100 == self.Player.GetBulletEnergy()) else Color.Black,
			self.Player.GetBulletEnergy(),

		)

		# Draw the bomb energy bar.

		DrawBar(

			screen,

			Vector(1 * barDimensions.X, barVerticalPosition),
			barDimensions,

			Color.Red if (100 == self.Player.GetBombEnergy()) else Color.Black,
			self.Player.GetBombEnergy(),

		)

		# Draw the shield energy bar.

		DrawBar(

			screen,

			Vector(2 * barDimensions.X, barVerticalPosition),
			barDimensions,

			Color.Blue,
			self.Player.GetShieldEnergy(),

		)