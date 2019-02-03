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

from Engine.Utilities.Color import Color
from Engine.Utilities.Vector import Vector

from numpy import random
from pygame import display, font, Surface, SRCALPHA

##
#
# Functions.
#
##

def Blit(surface, image, position = Vector()):

	surface.blit(image, tuple(position))

def GetDecision(possibilities):

	options, probabilities = zip(*possibilities.items())

	options = list(options)
	probabilities = list(probabilities)

	options.append(None)
	probabilities.append(1 - sum(probabilities))

	return random.choice(options, 1, p = probabilities)

def GetDimensions(surface):

	return Vector(surface.get_width(), surface.get_height())

def GetScreen():

	return display.get_surface()

def GetScreenDimensions():

	return GetDimensions(GetScreen())

def RenderText(text, font, color = Color.White):

	lines = text.splitlines()
	surfaces = [font.render(line, True, color) for line in lines]

	width = max([surface.get_width() for surface in surfaces])
	height = sum([surface.get_height() for surface in surfaces])

	destination = Surface([width, height], SRCALPHA, 32)
	verticalCursor = 0

	for surface in surfaces:
		destination.blit(surface, (0, verticalCursor))
		verticalCursor += surface.get_height()

	return destination