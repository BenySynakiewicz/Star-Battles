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
from Engine.World.Widgets.Bar import Bar
from Engine.World.Widgets.Label import Label
from Engine.Utilities.Direction import Direction
from Engine.Utilities.Vector import Vector
from Engine.Utilities.Color import Color
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, GetScreenDimensions, RenderText

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

		self._scoreLabel = Label(self, "No score is currently tracked", Resources().GetFont("Exo 2", Parameters.SmallTextHeight))
		self._scoreLabel.SetPosition(Vector(Parameters.Margin, Parameters.Margin))

		self._bonusLabel = Label(self, "No bonus is currently active", Resources().GetFont("Exo 2", Parameters.SmallTextHeight))
		self._bonusLabel.SetPosition(Vector(
			GetScreenDimensions().X - Parameters.Margin - self._bonusLabel.GetDimensions().X,
			Parameters.Margin
		))

		self.Append([self._scoreLabel, self._bonusLabel])

		# Initialize widgets.

		energyBarDimensions = Vector(GetScreenDimensions().X / 3, Parameters.BarHeight)
		energyBarVerticalPosition = GetScreenDimensions().Y - energyBarDimensions.Y

		self._bulletEnergyBar = Bar(self, Color.Black, Color.Green, energyBarDimensions)
		self._bombEnergyBar = Bar(self, Color.Black, Color.Red, energyBarDimensions)
		self._shieldEnergyBar = Bar(self, Color.Blue, Color.Blue, energyBarDimensions)

		self._bulletEnergyBar.SetPosition(Vector(0 * energyBarDimensions.X, energyBarVerticalPosition))
		self._bombEnergyBar.SetPosition(Vector(1 * energyBarDimensions.X, energyBarVerticalPosition))
		self._shieldEnergyBar.SetPosition(Vector(2 * energyBarDimensions.X, energyBarVerticalPosition))

		self.Append([self._bulletEnergyBar, self._bombEnergyBar, self._shieldEnergyBar])

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

		self._battleManager = BattleManager(self, 2 * Parameters.Margin + self._scoreLabel.GetDimensions().Y)

	def Show(self):

		mouse.set_visible(False)

	def UpdateScoreText(self):

		self._scoreLabel.SetText(f"{State().GetScoreManager().GetCurrentScore()} points")

	def UpdateBonusDescriptionText(self):

		bonusManager = self.Player.GetBonusManager()

		if bonusManager.IsAnyBonusActive():
			description = f"{bonusManager.GetActiveBonusName()} bonus is now active [{bonusManager.GetActiveBonusTime()} s left]"
		else:
			description = "No bonus is currently active"

		if self._bonusLabel.SetText(description):
			self._bonusLabel.SetPosition(Vector(
				GetScreenDimensions().X - Parameters.Margin - self._bonusLabel.GetDimensions().X,
				Parameters.Margin
			))

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

	# Updating.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		# Finish the game if the player has been destroyed.

		if self.Player._terminated:
			Resources()._backgrounds["Screenshot"] = Desaturate(GetScreen())
			self._nextScene = EndGameScene()
			return

		# Remove terminated nodes (and update the score).

		for node in self._nodes:

			if "Enemy" == type(node).__name__ and node.IsDestroyed():
				self.UpdateScoreText()

		self._nodes[:] = filter(lambda x: not x.IsTerminated(), self._nodes)

		# Update the battle manager.

		self._battleManager.Update(milisecondsPassed)

		# Update labels.

		self.UpdateScoreText()
		self.UpdateBonusDescriptionText()

		# Update energy bars.

		self._bulletEnergyBar.SetProgress(self.Player.GetBulletEnergy())
		self._bombEnergyBar.SetProgress(self.Player.GetBombEnergy())
		self._shieldEnergyBar.SetProgress(self.Player.GetShieldEnergy())

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