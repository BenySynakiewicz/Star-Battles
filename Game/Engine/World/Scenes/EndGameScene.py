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

from pygame import KEYDOWN, K_SPACE

##
#
# The main class.
#
##

class EndGameScene(Scene):

	def __init__(self):

		super().__init__("Background")

		State().SaveToFile()

		currentScore = State().GetCurrentScore()
		highestScore = State().GetHighestScore()

		self._title = RenderText(f"You've earned {currentScore} points!", Resources().GetFont("Title"))
		self._message = RenderText(
			f"Your record remains {highestScore} points."
				if currentScore < highestScore
				else
			f"You've beaten your previous record of {highestScore} points!",
			Resources().GetFont("Big")
		)
		self._instruction = RenderText(
			"Press the SPACE key to start the game one more time." "\n"
			"Press the ESC key to quit the game.",
			Resources().GetFont("Medium")
		)

	# Inherited methods.

	def React(self, events, keys):

		for event in [event for event in events if KEYDOWN == event.type]:

			if K_SPACE == event.key:
				self._nextScene = None#TitleScene()

	def Render(self):

		Scene.Render(self)

		# Retrieve the screen.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Calculate the positions of the texts.

		titlePosition = (screenDimensions - GetDimensions(self._title)) // 2

		messagePosition = (screenDimensions - GetDimensions(self._message)) // 2
		messagePosition.Y = titlePosition.Y + self._title.get_height()

		instructionPosition = Vector(Parameters.Margin, screenDimensions.Y - Parameters.Margin - self._instruction.get_height())

		# Blit the texts.

		Blit(screen, self._title, titlePosition)
		Blit(screen, self._message, messagePosition)
		Blit(screen, self._instruction, instructionPosition)