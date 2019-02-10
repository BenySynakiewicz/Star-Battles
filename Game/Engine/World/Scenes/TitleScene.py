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
from Engine.World.Scenes.BattleScene import BattleScene
from Engine.World.Widgets.Button import Button
from Engine.Utilities.Vector import Vector
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, RenderText

from sys import exit

from pygame import (
	mouse,
	KEYDOWN, MOUSEBUTTONDOWN,
)

##
#
# The main class.
#
##

class TitleScene(Scene):

	def __init__(self):

		super().__init__("Background")

		# Clear the game state (because we assume the game is being started anew).

		State().Clear()

		# Create texts and buttons.

		titleFont = Resources().GetFont("Exo 2 Light", Parameters.BigTextHeight)
		creatorFont = Resources().GetFont("Exo 2", Parameters.SmallTextHeight)
		buttonFont = Resources().GetFont("Exo 2 Light", Parameters.BiggishTextHeight)

		self._title = RenderText(Parameters.Name, titleFont)
		self._creator = RenderText(f"Created by {Parameters.Creator}" "\n" f"Version {Parameters.Version}", creatorFont, alignRight = True)

		self._newGameButton = Button(self, "New Game", buttonFont)
		self._quitButton = Button(self, "Quit", buttonFont)

		self.Append(self._newGameButton)
		self.Append(self._quitButton)

	# Inherited methods.

	def Show(self):

		mouse.set_visible(True)

	def React(self, events, _):

		for event in events:

			if MOUSEBUTTONDOWN == event.type:

				if self._newGameButton.IsBeingPointedAt():
					self._nextScene = BattleScene()
				elif self._quitButton.IsBeingPointedAt():
					exit()

	def Render(self):

		super().Render()

		# Retrieve the screen.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Calculate the positions of the texts.

		titlePosition = (screenDimensions - GetDimensions(self._title)) / 2
		titlePosition.Y = Parameters.HugeMargin

		creatorPosition = Vector(screenDimensions.X - GetDimensions(self._creator).X - Parameters.Margin, Parameters.Margin)

		self._newGameButton.SetPosition(Vector((screenDimensions.X - self._newGameButton.GetDimensions().X) / 2, titlePosition.Y + GetDimensions(self._title).Y + 4 * Parameters.Margin))
		self._quitButton.SetPosition(Vector((screenDimensions.X - self._quitButton.GetDimensions().X) / 2, self._newGameButton.GetPosition().Y + self._newGameButton.GetDimensions().Y + Parameters.Margin))

		# Blit the texts.

		Blit(screen, self._title, titlePosition)
		Blit(screen, self._creator, creatorPosition)