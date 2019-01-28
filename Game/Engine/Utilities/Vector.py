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
# The main class.
#
##

class Vector:

	def __init__(self, x = 0, y = 0):

		self.X = x
		self.Y = y

	def __iter__(self):

		return iter([self.X, self.Y])

	def __add__(self, vector):

		return Vector(self.X + vector.X, self.Y + vector.Y)

	def __sub__(self, vector):

		return Vector(self.X - vector.X, self.Y - vector.Y)

	def __mul__(self, scalar):

		return Vector(self.X * scalar, self.Y * scalar)

	def __floordiv__(self, scalar):

		return Vector(self.X // scalar, self.Y // scalar)

	def __truediv__(self, scalar):

		return Vector(self.X / scalar, self.Y / scalar)