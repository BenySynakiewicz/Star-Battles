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

from Engine.Utilities.General import GetScreenDimensions

##
#
# Functions.
#
##

def AtSameCenter(referencePosition, referenceDimensions, targetDimensions):

	referenceCenter = referencePosition + (referenceDimensions / 2)
	targetPosition = referenceCenter - (targetDimensions / 2)

	return targetPosition

def AtTop(referencePosition, referenceDimensions, targetDimensions):

	targetPosition = AtSameCenter(referencePosition, referenceDimensions, targetDimensions)
	targetPosition.Y = referencePosition.Y - targetDimensions.Y - 1

	return targetPosition

def AtBottom(referencePosition, referenceDimensions, targetDimensions):

	targetPosition = AtSameCenter(referencePosition, referenceDimensions, targetDimensions)
	targetPosition.Y = referencePosition.Y + targetDimensions.Y + 1

	return targetPosition

def IsOutsideScreen(position, dimensions):

	screenDimensions = GetScreenDimensions()

	isTopOfTheScreen = position.Y < -dimensions.Y
	if isTopOfTheScreen:
		return True

	isBottomOfTheScreen = position.Y > screenDimensions.Y
	if isBottomOfTheScreen:
		return True

	isLeftToTheScreen = position.X < -dimensions.X
	if isLeftToTheScreen:
		return True

	isRightToTheScreen = position.X > screenDimensions.X
	if isRightToTheScreen:
		return True

	return False