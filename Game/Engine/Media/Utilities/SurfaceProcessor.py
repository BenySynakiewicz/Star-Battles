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

from numpy import mean
from pygame import surfarray, transform

##
#
# Functions.
#
##

def Desaturate(surface):

	pixelData = surfarray.array3d(surface)
	pixelData = pixelData.dot([0.298, 0.587, 0.114])[:, :, None].repeat(3, axis = 2)

	return surfarray.make_surface(pixelData)

def InterpolateToDimensions(surface, dimensions):

	return transform.smoothscale(surface, tuple(dimensions))

def InterpolateToScale(surface, scale):

	dimensions = GetDimensions(surface) * scale

	dimensions.X = int(dimensions.X)
	dimensions.Y = int(dimensions.Y)

	return InterpolateToDimensions(surface, dimensions)