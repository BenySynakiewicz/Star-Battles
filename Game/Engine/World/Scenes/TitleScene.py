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

from pygame import mouse, KEYDOWN, MOUSEBUTTONDOWN

##
#
# The main class.
#
##

class TitleScene(Scene):

	def __init__(self):

		super().__init__("Background")

		State().Clear()

		self._title = RenderText(Parameters.Name, Resources().GetFont("Exo 2 Light", Parameters.BigTextHeight))
		self._creator = RenderText(
			f"Created by {Parameters.Creator}" "\n"
			f"Version {Parameters.Version}",
			font = Resources().GetFont("Exo 2", Parameters.SmallTextHeight),
			alignRight = True
		)

		self._newGameButton = Button(self, "New Game", Resources().GetFont("Exo 2 Light", Parameters.BiggishTextHeight))
		self._quitButton = Button(self, "Quit", Resources().GetFont("Exo 2 Light", Parameters.BiggishTextHeight))

	def Show(self):

		mouse.set_visible(True)

	def React(self, events, _):

		for event in events:

			if KEYDOWN == event.type:

				self._nextScene = BattleScene()

			elif MOUSEBUTTONDOWN == event.type:

				newGameButtonRectangle = self._newGameButton.GetRectangle()
				quitButtonRectangle = self._quitButton.GetRectangle()

				mouseCursorPosition = mouse.get_pos()

				if newGameButtonRectangle.collidepoint(mouseCursorPosition):
					self._nextScene = BattleScene()
				elif quitButtonRectangle.collidepoint(mouseCursorPosition):
					exit()

	def Render(self):

		Scene.Render(self)

		# Retrieve the screen.

		screen = GetScreen()
		screenDimensions = GetDimensions(screen)

		# Calculate the positions of the texts.

		titlePosition = (screenDimensions - GetDimensions(self._title)) // 2
		titlePosition.Y = 12 * Parameters.Margin

		creatorPosition = Vector(screenDimensions.X - GetDimensions(self._creator).X - Parameters.Margin, Parameters.Margin)

		self._newGameButton.SetPosition(Vector((screenDimensions.X - self._newGameButton.GetDimensions().X) / 2, titlePosition.Y + GetDimensions(self._title).Y + 4 * Parameters.Margin))
		self._quitButton.SetPosition(Vector((screenDimensions.X - self._quitButton.GetDimensions().X) / 2, self._newGameButton.GetPosition().Y + self._newGameButton.GetDimensions().Y + Parameters.Margin))

		# Blit the texts.

		Blit(screen, self._title, titlePosition)
		Blit(screen, self._creator, creatorPosition)

		self._newGameButton.Render()
		self._quitButton.Render()