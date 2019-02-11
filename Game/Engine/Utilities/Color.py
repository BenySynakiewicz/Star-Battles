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

from colorsys import rgb_to_hsv, hsv_to_rgb
from types import SimpleNamespace

##
#
# Globals.
#
##

Color = SimpleNamespace(

	Black    = (0  , 0  , 0  , 255),
	White    = (255, 255, 255, 255),

	Green = (25 , 255, 25 , 255),
	Red   = (255, 25 , 25 , 255),
	Blue  = (25 , 25 , 255, 255),

)

##
#
# Functions.
#
##

def InterpolateBetweenColors(firstColor, secondColor, progress):

	firstColorAsHSV = rgb_to_hsv(firstColor[0], firstColor[1], firstColor[2])
	secondColorAsHSV = rgb_to_hsv(secondColor[0], secondColor[1], secondColor[2])

	interpolatedColor = [0, 0, 0, 0]

	interpolatedColor[0] = LinearInterpolation(firstColorAsHSV[0], secondColorAsHSV[0], progress)
	interpolatedColor[1] = LinearInterpolation(firstColorAsHSV[1], secondColorAsHSV[1], progress)
	interpolatedColor[2] = LinearInterpolation(firstColorAsHSV[2], secondColorAsHSV[2], progress)
	interpolatedColor[3] = LinearInterpolation(firstColor[3], secondColor[3], progress)

	return (*hsv_to_rgb(interpolatedColor[0], interpolatedColor[1], interpolatedColor[2]), interpolatedColor[3])

def SetAlpha(color, alpha):

	return (color[0], color[1], color[2], alpha)

##
#
# Utilities.
#
##

def LinearInterpolation(a, b, progress):

	return a * (1 - progress) + b * progress