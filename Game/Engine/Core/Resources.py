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

		# Initialize the caches.

		self._fonts = {}
		self._sprites = {}
		self._backgrounds = {}
		self._sounds = {}

		# Load fonts.

		self._LoadFont("Title" , "Resources/Fonts/Exo 2 Light.ttf", 96)
		self._LoadFont("Big"   , "Resources/Fonts/Exo 2 Light.ttf", 48)
		self._LoadFont("Medium", "Resources/Fonts/Exo 2.ttf"      , 18)

		# Load backgrounds.

		self._LoadBackground("Background", "Resources/Images/Background.jpeg")

		# Load sprites.

		self._LoadSprite("Bullet (Green)", "Resources/Images/Bullet (Green).png")
		self._LoadSprite("Bullet (Red)", "Resources/Images/Bullet (Red).png")
		self._LoadSprite("Shield", "Resources/Images/Shield.png")
		self._LoadSprite("Bonus 1", "Resources/Images/Bonus 1/")
		self._LoadSprite("Bonus 2", "Resources/Images/Bonus 2/")
		self._LoadSprite("Bonus 3", "Resources/Images/Bonus 3/")
		self._LoadSprite("Bonus 4", "Resources/Images/Bonus 4/")
		self._LoadSprite("Player", "Resources/Images/Player/", shadows = True, framesPerSecond = 6)
		self._LoadSprite("Enemy", "Resources/Images/Enemy/", shadows = True, framesPerSecond = 6)
		self._LoadSprite("Bomb", "Resources/Images/Bomb/", shadows = True, framesPerSecond = 6)
		self._LoadSprite("Explosion", "Resources/Images/Explosion/")
		self._LoadSprite("Absorption", "Resources/Images/Absorption/")

		# Load sounds.

		self._LoadSound("Bomb", "Resources/Sounds/Bomb.ogg", range( 1,  3))
		self._LoadSound("Bullet", "Resources/Sounds/Bullet.ogg", range( 3, 17))
		self._LoadSound("Destruction", "Resources/Sounds/Destruction.ogg", range(18, 19))
		self._LoadSound("Explosion", "Resources/Sounds/Explosion.ogg", range(20, 21))
		self._LoadSound("Shield", "Resources/Sounds/Shield.ogg", range(22, 24))
		self._LoadSound("Absorption", "Resources/Sounds/Absorption.ogg", range(25, 26))

		# Load music.

		mixer.music.load("Resources/Sounds/Ambience.ogg")

	def GetFont(self, identifier):

		return self._fonts[identifier]

	def GetBackground(self, identifier):

		return self._backgrounds[identifier]

	def GetSprite(self, identifier, dimensions = None, rotation = None):

		return self._sprites[identifier].Get(dimensions, rotation)

	def GetSound(self, identifier):

		return self._sounds[identifier]

	def _LoadFont(self, name, path, height):

		self._fonts[name] = font.Font(path, height)

	def _LoadSprite(self, name, path, shadows = False, framesPerSecond = 40):

		self._sprites[name] = SpriteCollection(path, shadows, framesPerSecond)

	def _LoadBackground(self, name, path):

		self._backgrounds[name] = transform.smoothscale(image.load(path), tuple(GetScreenDimensions())).convert_alpha()

	def _LoadSound(self, name, path, channels):

		self._sounds[name] = Sound(path, channels)

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