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
from Engine.Utilities.General import Blit, GetDimensions, GetScreen, RenderText
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.Scene import Scene
from Engine.World.Scenes.BattleScene import BattleScene
from Engine.World.Widgets.Button import Button

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

		# Create texts.

		titleFont = Resources().GetFont("Exo 2 Light", Parameters.HugeTextHeight)
		creatorFont = Resources().GetFont("Exo 2", Parameters.SmallTextHeight)
		buttonFont = Resources().GetFont("Exo 2 Light", Parameters.MediumTextHeight)

		self._title = RenderText(Parameters.Name, titleFont)
		self._creator = RenderText(f"Created by {Parameters.Creator}", creatorFont)
		self._version = RenderText(f"Version {Parameters.Version}", creatorFont, alignRight = True)

		# Create buttons.

		self._newGameButton = Button(self, "New Game", buttonFont)
		self._quitButton = Button(self, "Quit", buttonFont)

		buttons = [self._newGameButton, self._quitButton]
		[x.SetMinimumWidth(Parameters.ButtonWidth) for x in buttons]

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

		# Calculate the positions of texts and buttons.

		titleDimensions = GetDimensions(self._title)
		creatorDimensions = GetDimensions(self._creator)
		versionDimensions = GetDimensions(self._version)
		newGameButtonDimensions = self._newGameButton.GetDimensions()
		quitButtonDimensions = self._newGameButton.GetDimensions()

		upperTextsHeight = max([creatorDimensions.Y, versionDimensions.Y])
		lowerButtonsHeight = max([newGameButtonDimensions.Y, quitButtonDimensions.Y])

		titlePosition = Vector(
			(screenDimensions.X - titleDimensions.X) / 2,
			(screenDimensions.Y - Parameters.Margin - lowerButtonsHeight - titleDimensions.Y + upperTextsHeight) / 2,
		)

		creatorPosition = Vector(
			Parameters.Margin,
			Parameters.Margin,
		)

		versionPosition = Vector(
			screenDimensions.X - versionDimensions.X - Parameters.Margin,
			Parameters.Margin,
		)

		self._newGameButton.SetPosition(Vector(
			Parameters.Margin,
			screenDimensions.Y - Parameters.Margin - newGameButtonDimensions.Y,
		))

		self._quitButton.SetPosition(Vector(
			screenDimensions.X - Parameters.Margin - quitButtonDimensions.X,
			screenDimensions.Y - Parameters.Margin - quitButtonDimensions.Y,
		))

		# Blit the texts.

		Blit(screen, self._title, titlePosition)
		Blit(screen, self._creator, creatorPosition)
		Blit(screen, self._version, versionPosition)