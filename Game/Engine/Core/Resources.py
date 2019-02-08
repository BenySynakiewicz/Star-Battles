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

from pathlib import Path
from types import SimpleNamespace

from pygame import image, font, mixer, transform

##
#
# The main class.
#
##

class Resources(metaclass = Singleton):

	def __init__(self):

		self.Paths = SimpleNamespace(
			Fonts = None,
			Sprites = None,
			Backgrounds = None,
			Sounds = None,
			Music = None,
		)

		self._fonts = {}
		self._sprites = {}
		self._backgrounds = {}
		self._sounds = {}

	def LoadFont(self, path):

		loadingPath = str(Path(self.Paths.Fonts) / path) if self.Paths.Fonts else path

		self._fonts[path] = FontCollection(loadingPath)

	def LoadSprite(self, path, shadows = False, framesPerSecond = 40):

		loadingPath = str(Path(self.Paths.Sprites) / path) if self.Paths.Sprites else path

		self._sprites[path] = SpriteCollection(loadingPath, shadows, framesPerSecond)

	def LoadBackground(self, path):

		loadingPath = str(Path(self.Paths.Backgrounds) / path) if self.Paths.Backgrounds else path

		self._backgrounds[path] = transform.smoothscale(image.load(loadingPath), tuple(GetScreenDimensions())).convert_alpha()

	def LoadSound(self, path, channels):

		loadingPath = str(Path(self.Paths.Sounds) / path) if self.Paths.Sounds else path

		self._sounds[path] = Sound(loadingPath, channels)

	def LoadMusic(self, path):

		loadingPath = str(Path(self.Paths.Music) / path) if self.Paths.Music else path

		mixer.music.load(loadingPath)

	def GetFont(self, path, height):

		return GetFromDictionary(self._fonts, path, [".ttf"]).Get(height)

	def GetBackground(self, path):

		return GetFromDictionary(self._backgrounds, path, [".jpeg"])

	def GetSprite(self, path, dimensions = None, rotation = None):

		return GetFromDictionary(self._sprites, path, [".png"]).Get(dimensions, rotation)

	def GetSound(self, path):

		return GetFromDictionary(self._sounds, path, [".ogg"])

##
#
# Utilities.
#
##

def GetFromDictionary(dictionary, key, suffixes):

	suffixes = [""] + suffixes

	for suffix in suffixes:

		completedKey = key + suffix
		if completedKey in dictionary:
			return dictionary[completedKey]

	return None

##
#
# Classes.
#
##

class FontCollection:

	def __init__(self, path):

		self._path = path
		self._variants = {}

	def Get(self, height):

		if height not in self._variants:
			self._variants[height] = font.Font(self._path, height)

		return self._variants[height]

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