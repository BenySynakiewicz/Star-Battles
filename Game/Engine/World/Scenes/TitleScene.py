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
from Engine.World.Concepts.Scene import Scene
from Engine.World.Scenes.BattleScene import BattleScene
from Engine.Utilities.Vector import Vector
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, RenderText

from pygame import KEYDOWN

##
#
# The main class.
#
##

class TitleScene(Scene):

	def __init__(self):

		super().__init__("Background")

		self._title = RenderText(Parameters.Name, Resources().GetFont("Title"))
		self._message = RenderText("Press any key to begin the game", Resources().GetFont("Big"))
		self._creator = RenderText(f"Created by {Parameters.Creator}", Resources().GetFont("Medium"))
		self._version = RenderText(f"Version {Parameters.Version}", Resources().GetFont("Medium"))
		self._instruction = RenderText(
			"Press the UP arrow key to shoot a bullet." "\n"
			"Press the LEFT and RIGHT arrow keys to move." "\n"
			"Press the SPACE key to shoot a bomb." "\n"
			"Press the SPACE key again to detonate the bomb." "\n"
			"Press the DOWN arrow key to activate the shield.",
			Resources().GetFont("Medium")
		)

	def React(self, events, _):

		if any(KEYDOWN == event.type for event in events):
			self._nextScene = BattleScene()

	def Render(self):

		Scene.Render(self)

		# Retrieve the screen.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Calculate the positions of the texts.

		titlePosition = (screenDimensions - GetDimensions(self._title)) // 2
		titlePosition.Y -= GetDimensions(self._message).Y // 2

		messagePosition = (screenDimensions - GetDimensions(self._message)) // 2
		messagePosition.Y = titlePosition.Y + self._title.get_height()

		creatorPosition = Vector(Parameters.Margin, Parameters.Margin)
		versionPosition = Vector(screenDimensions.X - self._version.get_width() - Parameters.Margin, Parameters.Margin)
		instructionPosition = Vector(Parameters.Margin, screenDimensions.Y - Parameters.Margin - self._instruction.get_height())

		# Blit the texts.

		Blit(screen, self._title, titlePosition)
		Blit(screen, self._message, messagePosition)
		Blit(screen, self._creator, creatorPosition)
		Blit(screen, self._version, versionPosition)
		Blit(screen, self._instruction, instructionPosition)