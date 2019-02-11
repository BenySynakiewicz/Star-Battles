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
from Engine.Media.Concepts.SpriteInstance import SpriteInstance
from Engine.Utilities.General import GetDimensions, GetScreen
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Scene import Scene
from Engine.World.Scenes.BattleScene import BattleScene
from Engine.World.Utilities.WidgetPositioners import MoveToTheBottom, SpreadHorizontally
from Engine.World.Widgets.Button import Button
from Engine.World.Widgets.Label import Label

from sys import exit

from pygame import MOUSEBUTTONDOWN

##
#
# The main class.
#
##

class TitleScene(Scene):

	# The constructor.

	def __init__(self):

		# Initialize the scene.

		super().__init__("Background")

		self._cursor = SpriteInstance(Resources().GetSprite("Cursor"))

		# Clear the game state (we assume the game is being started anew).

		State().Clear()

		# Create fonts for labels and buttons.

		titleFont = Resources().GetFont("Exo 2 Light", Parameters.HugeTextHeight)
		creatorFont = Resources().GetFont("Exo 2", Parameters.SmallTextHeight)
		buttonFont = Resources().GetFont("Exo 2 Light", Parameters.MediumTextHeight)

		# Create labels.

		self._title = Label(self, Parameters.Name, titleFont)
		self._creator = Label(self, f"Created by {Parameters.Creator}", creatorFont)
		self._version = Label(self, f"Version {Parameters.Version}", creatorFont)

		labels = [self._title, self._creator, self._version]

		# Create buttons.

		self._newGameButton = Button(self, "New Game", buttonFont, minimumWidth = Parameters.ButtonWidth)
		self._newGameButton.SetOnClickFunction(self.FinishScene)

		self._quitButton = Button(self, "Quit", buttonFont, minimumWidth = Parameters.ButtonWidth)
		self._quitButton.SetOnClickFunction(self.QuitGame)

		buttons = [self._newGameButton, self._quitButton]

		# Append and position the widgets.

		self.Append(labels + buttons)

		self._PositionWidgets()

	# Operations.

	def FinishScene(self):

		self._nextScene = BattleScene()

	def QuitGame(self):

		exit()

	# Reacting.

	def React(self, events, _):

		for event in [x for x in events if MOUSEBUTTONDOWN == x.type]:

			if self._newGameButton.IsBeingPointedAt(): self._newGameButton.Click()
			elif self._quitButton.IsBeingPointedAt(): self._quitButton.Click()

	# Utilities.

	def _PositionWidgets(self):

		# Retrieve the screen and its dimensions.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Position the top labels.

		labels = [self._creator, self._version]

		SpreadHorizontally(screen, labels, Parameters.Margin, Parameters.Margin)

		# Position the buttons.

		buttons = [self._newGameButton, self._quitButton]

		SpreadHorizontally(screen, buttons, 0, Parameters.Margin)
		MoveToTheBottom(screen, buttons, Parameters.Margin)

		# Position the title.

		labelsPartHeight = Parameters.Margin + max([x.GetDimensions().Y for x in labels])
		buttonsPartHeight = Parameters.Margin + max([x.GetDimensions().Y for x in buttons])

		titleDimensions = self._title.GetDimensions()

		self._title.SetPosition(Vector(
			(screenDimensions - titleDimensions).X / 2,
			labelsPartHeight + (screenDimensions.Y - titleDimensions.Y - labelsPartHeight - buttonsPartHeight) / 2,
		))