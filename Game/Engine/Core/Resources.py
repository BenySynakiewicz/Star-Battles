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

from Engine.Media.Concepts.Sound import Sound
from Engine.Media.Concepts.Sprite import Sprite
from Engine.Utilities.Singleton import Singleton
from Engine.Utilities.General import GetScreenDimensions
from Engine.Utilities.Vector import Vector

from pygame import image, font, mixer, transform

##
#
# The main class.
#
##

class Resources(metaclass = Singleton):

	def __init__(self):

		self._fonts = {}
		self._sprites = {}
		self._backgrounds = {}
		self._sounds = {}

	def LoadFont(self, name, path, height):

		self._fonts[name] = font.Font(path, height)

	def LoadSprite(self, name, path, shadows = False, framesPerSecond = 40):

		self._sprites[name] = SpriteCollection(path, shadows, framesPerSecond)

	def LoadBackground(self, name, path):

		self._backgrounds[name] = transform.smoothscale(image.load(path), tuple(GetScreenDimensions())).convert_alpha()

	def LoadSound(self, name, path, channels):

		self._sounds[name] = Sound(path, channels)

	def LoadMusic(self, path):

		mixer.music.load(path)

	def GetFont(self, identifier):

		return self._fonts[identifier]

	def GetBackground(self, identifier):

		return self._backgrounds[identifier]

	def GetSprite(self, identifier, dimensions = None, rotation = None):

		return self._sprites[identifier].Get(dimensions, rotation)

	def GetSound(self, identifier):

		return self._sounds[identifier]

##
#
# Classes.
#
##

class SpriteCollection:

	def __init__(self, path, shadows = False, framesPerSecond = 40):

		self._source = Sprite(path, shadows, framesPerSecond)
		self._variants = {}

	def Get(self, dimensions = None, rotation = None):

		if not dimensions and not rotation:
			return self._source

		sourceDimensions = self._source.GetDimensions()
		sourceRotation = 0

		if dimensions == sourceDimensions and rotation == sourceRotation:
			return self._source

		variant = (dimensions, rotation)
		if variant in self._variants:
			return self._variants[variant]

		newVariant = None
		if (dimensions and dimensions != sourceDimensions) and (rotation and rotation != sourceRotation):
			newVariant = self._source.GetScaledCopy(dimensions)
			newVariant = newVariant.GetRotatedCopy(rotation)
		elif dimensions and dimensions != sourceDimensions:
			newVariant = self._source.GetScaledCopy(dimensions)
		elif rotation and rotation != sourceRotation:
			newVariant = self._source.GetRotatedCopy(rotation)

		self._variants[variant] = newVariant

		return self._variants[variant]