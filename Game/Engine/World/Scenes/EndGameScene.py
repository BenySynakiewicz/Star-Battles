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
from Engine.Utilities.Vector import Vector
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, RenderText
from Engine.World.Concepts.Scene import Scene
from Engine.World.Widgets.Button import Button

from pygame import (
	mouse,
	KEYDOWN, K_SPACE,
	MOUSEBUTTONDOWN,
)

##
#
# The main class.
#
##

class EndGameScene(Scene):

	def __init__(self):

		super().__init__("Screenshot")

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

		self._title = RenderText(titleMessage, titleFont)
		self._message = RenderText(message, messageFont)

		buttonFont = Resources().GetFont("Exo 2 Light", Parameters.BiggishTextHeight)

		self._continueButton = Button(self, "Continue", buttonFont)
		self.Append(self._continueButton)

	# Inherited methods.

	def Show(self):

		mouse.set_visible(True)

	def React(self, events, keys):

		# for event in events:

			# if (KEYDOWN == event.type and K_SPACE == event.key) or MOUSEBUTTONDOWN == event.type:

				# self._nextScene = None

				# return

		for event in events:

			if MOUSEBUTTONDOWN == event.type:

				if self._continueButton.IsBeingPointedAt():
					self._nextScene = None

	def Render(self):

		Scene.Render(self)

		# Retrieve the screen.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Calculate the positions of the texts.

		titlePosition = (screenDimensions - GetDimensions(self._title)) // 2
		titlePosition.Y = Parameters.HugeMargin

		messagePosition = (screenDimensions - GetDimensions(self._message)) // 2
		messagePosition.Y = titlePosition.Y + self._title.get_height()

		self._continueButton.SetPosition(Vector((screenDimensions.X - self._continueButton.GetDimensions().X) / 2, messagePosition.Y + GetDimensions(self._message).Y + 4 * Parameters.Margin))

		# Position the continue button.

		# Blit the texts.

		Blit(screen, self._title, titlePosition)
		Blit(screen, self._message, messagePosition)