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
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, RenderText
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Scene import Scene
from Engine.World.Widgets.Button import Button
from Engine.World.Widgets.Label import Label

from pygame import MOUSEBUTTONDOWN

##
#
# The main class.
#
##

class EndGameScene(Scene):

	# The constructor.

	def __init__(self):

		# Initialize the scene.

		super().__init__("Screenshot")

		self._cursor = SpriteInstance(Resources().GetSprite("Cursor"))

		# Save the game state.

		State().SaveToFile()

		# Prepare the texts.

		scoreManager = State().GetScoreManager()
		currentScore = scoreManager.GetCurrentScore()
		highestScore = scoreManager.GetHighestScore()

		titleMessage = f"You've earned {currentScore} points!"
		message = (
			f"Your record remains {highestScore} points."
			if currentScore < highestScore else
			f"You've beaten your previous record of {highestScore} points!"
		)

		# Initialize the texts and the buttons.

		titleFont = Resources().GetFont("Exo 2 Light", Parameters.BigTextHeight)
		messageFont = Resources().GetFont("Exo 2 Light", Parameters.MediumTextHeight)
		buttonFont = Resources().GetFont("Exo 2 Light", Parameters.MediumTextHeight)

		self._titleLabel = Label(self, titleMessage, titleFont)
		self._messageLabel = Label(self, message, messageFont)

		self._continueButton = Button(self, "Continue", buttonFont)
		self._continueButton.SetMinimumWidth(Parameters.ButtonWidth)

		self.Append([self._titleLabel, self._messageLabel, self._continueButton])

		# Position the widgets.

		self._PositionWidgets()

	# Reactions.

	def React(self, events, keys):

		for event in events:

			if MOUSEBUTTONDOWN == event.type:

				if self._continueButton.IsBeingPointedAt():
					self._continueButton.Click()
					self._nextScene = None

	# Utilities.

	def _PositionWidgets(self):

		# Retrieve the screen.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Calculate the positions of texts and buttons.

		titleDimensions = self._titleLabel.GetDimensions()
		messageDimensions = self._messageLabel.GetDimensions()
		continueButtonDimensions = self._continueButton.GetDimensions()

		titleAndMessageBundleHeight = titleDimensions.Y + messageDimensions.Y

		self._titleLabel.SetPosition(Vector(
			(screenDimensions.X - titleDimensions.X) / 2,
			(screenDimensions.Y - Parameters.Margin - continueButtonDimensions.Y - titleAndMessageBundleHeight) / 2,
		))

		self._messageLabel.SetPosition(Vector(
			(screenDimensions.X - messageDimensions.X) / 2,
			self._titleLabel.GetPosition().Y + titleDimensions.Y,
		))

		self._continueButton.SetPosition(Vector(
			(screenDimensions.X - continueButtonDimensions.X) / 2,
			screenDimensions.Y - Parameters.Margin - continueButtonDimensions.Y,
		))