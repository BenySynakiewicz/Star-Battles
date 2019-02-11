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

from Engine.Utilities.General import GetDimensions
from Engine.Utilities.Vector import Vector

##
#
# Functions.
#
##

def MoveToTheBottom(destinationSurface, widgets, margin = None):

	destinationDimensions = GetDimensions(destinationSurface)

	for widget in widgets:

		position = widget.GetPosition()
		dimensions = widget.GetDimensions()

		position.Y = destinationDimensions.Y - (margin if margin else 0) - dimensions.Y

		widget.SetPosition(position)

def SpreadHorizontally(destinationSurface, widgets, verticalPosition, margin = None):

	destinationDimensions = GetDimensions(destinationSurface)
	if margin:
		destinationDimensions.X -= 2 * margin

	widgetDimensions = [x.GetDimensions() for x in widgets]

	totalWidth = sum([x.X for x in widgetDimensions])

	spaceCount = len(widgets) - 1
	spaceWidth = (destinationDimensions.X - totalWidth) / spaceCount

	sumOfWidths = 0
	numberOfSpaces = 0

	for index in range(len(widgets)):

		currentPosition = (0 if not margin else margin) + sumOfWidths + numberOfSpaces * spaceWidth
		position = Vector(currentPosition, verticalPosition)

		widgets[index].SetPosition(position)

		sumOfWidths += widgetDimensions[index].X
		numberOfSpaces += 1