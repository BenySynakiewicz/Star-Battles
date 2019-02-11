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

from Engine.Utilities.Language import IsIndexable

from math import atan2, cos, degrees, hypot, radians, sin

##
#
# The main class.
#
##

class Vector:

	# The constructor.

	def __init__(self, x = 0, y = 0):

		self.X = x
		self.Y = y

	# Utilities.

	def GetLength(self):

		return hypot(self.X, self.Y)

	def GetAngle(self):

		vector = Vector(0, 1)

		dotProduct = vector.X * self.X + vector.Y * self.Y
		determinant = vector.X * self.Y - vector.Y * self.X

		return degrees(atan2(determinant, dotProduct))

	def GetNormalized(self):

		return self / self.GetLength()

	def GetRotatedAround(self, pivot, angle):

		angle = radians(-angle)
		sinus, cosinus = sin(angle), cos(angle)

		pivoted = self - pivot
		rotated = pivot + Vector(cosinus * pivoted.X - sinus * pivoted.Y, sinus * pivoted.X + cosinus * pivoted.Y)

		return rotated

	# Iterability.

	def __iter__(self):

		return iter([self.X, self.Y])

	# Equality.

	def __key(self):
		return (self.X, self.Y)

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		return isinstance(self, type(other)) and self.__hash__() == other.__hash__()

	# Indexability.

	def __getitem__(self, index):

		return [self.X, self.Y][index]

	def __len__(self):

		return 2

	# Arithmetic operations.

	def __neg__(self):

		return Vector(-self.X, -self.Y)

	def __add__(self, value):

		if IsIndexable(value) and len(value) > 1:
			return Vector(self.X + value[0], self.Y + value[1])

		return Vector(self.X + value, self.Y + value)

	def __sub__(self, value):

		if IsIndexable(value) and len(value) > 1:
			return Vector(self.X - value[0], self.Y - value[1])

		return Vector(self.X - value, self.Y - value)

	def __mul__(self, value):

		if IsIndexable(value) and len(value) > 1:
			return Vector(self.X * value[0], self.Y * value[1])

		return Vector(self.X * value, self.Y * value)

	def __floordiv__(self, value):

		if IsIndexable(value) and len(value) > 1:
			return Vector(self.X // value[0], self.Y // value[1])

		return Vector(self.X // value, self.Y // value)

	def __truediv__(self, value):

		if IsIndexable(value) and len(value) > 1:
			return Vector(self.X / value[0], self.Y / value[1])

		return Vector(self.X / value, self.Y / value)