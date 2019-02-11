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
from Engine.Utilities.General import GetScreenDimensions
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Scene import Scene
from Engine.World.Scenes.BattleScene import BattleScene
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

		super().__init__("Background")

		# Clear the game state (because we assume the game is being started anew).

		State().Clear()

		# Create texts.

		titleFont = Resources().GetFont("Exo 2 Light", Parameters.HugeTextHeight)
		creatorFont = Resources().GetFont("Exo 2", Parameters.SmallTextHeight)
		buttonFont = Resources().GetFont("Exo 2 Light", Parameters.MediumTextHeight)

		# Create labels.

		self._titleLabel = Label(self, Parameters.Name, titleFont)
		self._creatorLabel = Label(self, f"Created by {Parameters.Creator}", creatorFont)
		self._versionLabel = Label(self, f"Version {Parameters.Version}", creatorFont)

		labels = [self._titleLabel, self._creatorLabel, self._versionLabel]

		self.Append(labels)

		# Create buttons.

		self._newGameButton = Button(self, "New Game", buttonFont)
		self._quitButton = Button(self, "Quit", buttonFont)

		buttons = [self._newGameButton, self._quitButton]
		[x.SetMinimumWidth(Parameters.ButtonWidth) for x in buttons]

		self.Append(buttons)

		# Position the widgets.

		self._PositionWidgets()

	# Operations..

	def Show(self):

		self._cursor = SpriteInstance(Resources().GetSprite("Cursor"))

	# Reacting.

	def React(self, events, _):

		for event in events:

			if MOUSEBUTTONDOWN == event.type:

				if self._newGameButton.IsBeingPointedAt():
					self._newGameButton.Click()
					self._nextScene = BattleScene()
				elif self._quitButton.IsBeingPointedAt():
					self._quitButton.Click()
					exit()

	# Utilities.

	def _PositionWidgets(self):

		# Retrieve the screen dimensions.

		screenDimensions = GetScreenDimensions()

		# Calculate the positions of texts and buttons.

		titleDimensions = self._titleLabel.GetDimensions()
		creatorDimensions = self._creatorLabel.GetDimensions()
		versionDimensions = self._versionLabel.GetDimensions()
		newGameButtonDimensions = self._newGameButton.GetDimensions()
		quitButtonDimensions = self._newGameButton.GetDimensions()

		upperTextsHeight = max([creatorDimensions.Y, versionDimensions.Y])
		lowerButtonsHeight = max([newGameButtonDimensions.Y, quitButtonDimensions.Y])

		self._titleLabel.SetPosition(Vector(
			(screenDimensions.X - titleDimensions.X) / 2,
			(screenDimensions.Y - Parameters.Margin - lowerButtonsHeight - titleDimensions.Y + upperTextsHeight) / 2,
		))

		self._creatorLabel.SetPosition(Vector(
			Parameters.Margin,
			Parameters.Margin,
		))

		self._versionLabel.SetPosition(Vector(
			screenDimensions.X - versionDimensions.X - Parameters.Margin,
			Parameters.Margin,
		))

		self._newGameButton.SetPosition(Vector(
			Parameters.Margin,
			screenDimensions.Y - Parameters.Margin - newGameButtonDimensions.Y,
		))

		self._quitButton.SetPosition(Vector(
			screenDimensions.X - Parameters.Margin - quitButtonDimensions.X,
			screenDimensions.Y - Parameters.Margin - quitButtonDimensions.Y,
		))