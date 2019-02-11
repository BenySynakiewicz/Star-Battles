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

from pygame import gfxdraw, Surface, Rect, SRCALPHA, draw, transform, BLEND_RGBA_MAX, BLEND_RGBA_MIN

##
#
# Functions.
#
##

def RenderRoundedRectangle(surface, position, dimensions, color, radius = 0.5):

	targetRectangle = Rect(tuple(position), tuple(dimensions))

	alpha = color[3]
	color = (color[0], color[1], color[2], 0)

	position = targetRectangle.topleft
	targetRectangle.topleft = 0,0

	circle = Surface([min(targetRectangle.size) * 3] * 2, SRCALPHA)
	draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)

	circle = transform.smoothscale(circle, [int(min(targetRectangle.size) * radius)] * 2)

	rectangle = Surface(targetRectangle.size, SRCALPHA)
	radius = rectangle.blit(circle, (0, 0))

	radius.bottomright  = targetRectangle.bottomright
	rectangle.blit(circle, radius)

	radius.topright = targetRectangle.topright
	rectangle.blit(circle, radius)

	radius.bottomleft = targetRectangle.bottomleft
	rectangle.blit(circle, radius)

	rectangle.fill((0, 0, 0), targetRectangle.inflate(-radius.w, 0))
	rectangle.fill((0, 0, 0), targetRectangle.inflate(0, -radius.h))

	rectangle.fill(color, special_flags = BLEND_RGBA_MAX)
	rectangle.fill((255, 255, 255, alpha), special_flags = BLEND_RGBA_MIN)

	return surface.blit(rectangle, position)