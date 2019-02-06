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

from math import atan2, cos, pow, radians, sin, sqrt

##
#
# The main class.
#
##

class Vector:

	def __init__(self, x = 0, y = 0):

		self.X = x
		self.Y = y

	def GetAngle(self):

		vector = Vector(0, 1)

		dotProduct = vector.X * self.X + vector.Y * self.Y
		determinant = vector.X * self.Y - vector.Y * self.X

		return atan2(determinant, dotProduct)

	def GetNormalized(self):

		length = sqrt(pow(self.X, 2) + pow(self.Y, 2))

		return Vector(self.X / length, self.Y / length)

	def GetRotatedAround(self, pivot, angle):

		if not angle:
			return Vector(self.X, self.Y)

		angle = radians(-angle)

		sinus = sin(angle)
		cosinus = cos(angle)

		temporaryRotatedX = self.X - pivot.X
		temporaryRotatedY = self.Y - pivot.Y

		rotatedX = (temporaryRotatedX * cosinus) - (temporaryRotatedY * sinus) + pivot.X
		rotatedY = (temporaryRotatedX * sinus) + (temporaryRotatedY * cosinus) + pivot.Y

		return Vector(rotatedX, rotatedY)

	def __iter__(self):

		return iter([self.X, self.Y])

	def __key(self):
		return (self.X, self.Y)

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		return isinstance(self, type(other)) and self.__key() == other.__key()

	# def __eq__(self, vector):

		# if isinstance(vector, Vector):
			# return self.X == vector.X and self.Y == vector.Y

		# return False

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