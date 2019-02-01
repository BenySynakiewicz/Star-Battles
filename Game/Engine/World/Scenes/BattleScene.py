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
from Engine.World.Concepts.Scene import Scene
from Engine.World.Nodes.Effects.AbsorptionEffect import AbsorptionEffect
from Engine.World.Nodes.Player import Player
from Engine.World.Nodes.Enemy import Enemy
from Engine.World.Scenes.EndGameScene import EndGameScene
from Engine.Utilities.Direction import Direction
from Engine.Utilities.Vector import Vector
from Engine.Utilities.Color import Color
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, GetScreenDimensions, RenderText
from Engine.Utilities.GUI import DrawBar

from pygame import KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE

##
#
# The main class.
#
##

class BattleScene(Scene):

	def __init__(self):

		super().__init__("Background")

		self.ScoreText = None
		self.UpdateScoreText()

		# Initialize the player.

		self.Player = Player(self)

		screenDimensions = GetScreenDimensions()
		self.Player._position = Vector(

			(screenDimensions.X - self.Player.GetDimensions().X) / 2,
			(screenDimensions.Y - self.Player.GetDimensions().Y - 2 * Parameters.Margin - Parameters.BarHeight),

		)

		self.AppendNode(self.Player)
		self.AppendTimer("Enemy")

	def UpdateScoreText(self):

		self.ScoreText = RenderText(f"{State().GetCurrentScore()} points", Resources().GetFont("Medium"))

	def SpawnEnemies(self):

		currentScore = State().GetCurrentScore()
		verticalOffset = 2 * Parameters.Margin + GetDimensions(self.ScoreText).Y

		# In the first row...

		self.AppendNode(Enemy(self, verticalOffset, 0, Direction.Right))

		# In the sceond row...

		if currentScore >= 100:
			self.AppendNode(Enemy(self, verticalOffset, 1, Direction.Left))

		# In the third row...

		if currentScore >= 500:
			self.AppendNode(Enemy(self, verticalOffset, 2, Direction.Right))

		# In the fourth row...

		if currentScore >= 1500:
			self.AppendNode(Enemy(self, verticalOffset, 3, Direction.Left))

		# Clear the timer.

		self.ClearTimer("Enemy")

	def React(self, events, keys):

		# Process events.

		for event in [event for event in events if KEYDOWN == event.type]:

			if K_UP == event.key:
				self.Player.Shoot()

			elif K_SPACE == event.key:
				self.Player.ShootBomb()

		# Process pressed keys.

		if keys[K_LEFT]:
			self.Player.Move(Direction.Left)

		elif keys[K_RIGHT]:
			self.Player.Move(Direction.Right)

		self.Player.ShieldIsUp = bool(keys[K_DOWN])

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		# Finish the game if the player has been destroyed.

		if self.Player._terminated:
			self._nextScene = EndGameScene()
			return

		# Add enemies.

		if self.GetTimer("Enemy") // 1000 > 0:
			self.SpawnEnemies()

		# Remove terminated nodes (and update the score).

		for node in self._nodes:

			if node._terminated and "Enemy" == type(node).__name__ and node.DestroyedByPlayer:
				State().UpdateCurrentScore(+Parameters.EnemyValue)
				self.UpdateScoreText()

			if node._terminated and "Cargo" == type(node).__name__:
				State().UpdateCurrentScore(+Parameters.CargoValue)
				self.UpdateScoreText()

		self._nodes[:] = filter(lambda node: not node._terminated, self._nodes)

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

		Blit(screen, self.ScoreText, Vector(Parameters.Margin, Parameters.Margin))

		# Calculate the bar dimensions.

		barDimensions = Vector((screenDimensions.X - 4 * Parameters.Margin) / 3, Parameters.BarHeight)
		barVerticalPosition = screenDimensions.Y - Parameters.Margin - barDimensions.Y

		# Draw the bullet energy bar.

		DrawBar(

			screen,

			Vector(Parameters.Margin, barVerticalPosition),
			barDimensions,

			Color.Green if (100 == self.Player.Energy.Bullet) else Color.Black,
			self.Player.Energy.Bullet,

		)

		# Draw the bomb energy bar.

		DrawBar(

			screen,

			Vector(Parameters.Margin + 1 * (barDimensions.X + Parameters.Margin), barVerticalPosition),
			barDimensions,

			Color.Red if (100 == self.Player.Energy.Bomb) else Color.Black,
			self.Player.Energy.Bomb,

		)

		# Draw the shield energy bar.

		DrawBar(

			screen,

			Vector(Parameters.Margin + 2 * (barDimensions.X + Parameters.Margin), barVerticalPosition),
			barDimensions,

			Color.Blue,
			self.Player.Energy.Shield,

		)