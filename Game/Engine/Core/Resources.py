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

		self._fonts = {
			"Title" : font.Font("Resources/Fonts/Exo 2 Light.ttf", 96),
			"Big"   : font.Font("Resources/Fonts/Exo 2 Light.ttf", 48),
			"Medium": font.Font("Resources/Fonts/Exo 2.ttf"      , 18),
		}

		self._backgrounds = {
			"Background": LoadBackground("Resources/Images/Background.jpeg"),
		}

		self._sprites = {

			"Bullet (Green)": Sprite(["Resources/Images/Bullet (Green).png"]),
			"Bullet (Red)"  : Sprite(["Resources/Images/Bullet (Red).png"]  ),
			"Shield"        : Sprite(["Resources/Images/Shield.png"]        ),
			"Cargo"         : Sprite(["Resources/Images/Cargo.png"]         , True),

			"Bonus 1": Sprite([
				"Resources/Images/Bonus 1/1.png",
				"Resources/Images/Bonus 1/2.png",
				"Resources/Images/Bonus 1/3.png",
				"Resources/Images/Bonus 1/4.png",
				"Resources/Images/Bonus 1/5.png",
				"Resources/Images/Bonus 1/6.png",
			]),

			"Bonus 2": Sprite([
				"Resources/Images/Bonus 2/1.png",
				"Resources/Images/Bonus 2/2.png",
				"Resources/Images/Bonus 2/3.png",
				"Resources/Images/Bonus 2/4.png",
				"Resources/Images/Bonus 2/5.png",
				"Resources/Images/Bonus 2/6.png",
			]),

			"Bonus 3": Sprite([
				"Resources/Images/Bonus 3/1.png",
				"Resources/Images/Bonus 3/2.png",
				"Resources/Images/Bonus 3/3.png",
				"Resources/Images/Bonus 3/4.png",
				"Resources/Images/Bonus 3/5.png",
				"Resources/Images/Bonus 3/6.png",
			]),

			"Bonus 4": Sprite([
				"Resources/Images/Bonus 4/1.png",
				"Resources/Images/Bonus 4/2.png",
				"Resources/Images/Bonus 4/3.png",
				"Resources/Images/Bonus 4/4.png",
				"Resources/Images/Bonus 4/5.png",
				"Resources/Images/Bonus 4/6.png",
			]),

			"Player": Sprite([
				"Resources/Images/Player/1.png",
				"Resources/Images/Player/2.png",
				"Resources/Images/Player/3.png",
				"Resources/Images/Player/4.png",
				"Resources/Images/Player/5.png",
				"Resources/Images/Player/6.png",
				"Resources/Images/Player/7.png",
				"Resources/Images/Player/8.png",
			], True, framesPerSecond = 6),

			"Enemy": Sprite([
				"Resources/Images/Enemy/1.png",
				"Resources/Images/Enemy/2.png",
				"Resources/Images/Enemy/3.png",
				"Resources/Images/Enemy/4.png",
				"Resources/Images/Enemy/5.png",
			], True, framesPerSecond = 6),

			"Bomb": Sprite([
				"Resources/Images/Bomb/1.png",
				"Resources/Images/Bomb/2.png",
				"Resources/Images/Bomb/3.png",
			], True, framesPerSecond = 6),

			"Explosion": Sprite([
				"Resources/Images/Explosion/1.png",
				"Resources/Images/Explosion/2.png",
				"Resources/Images/Explosion/3.png",
				"Resources/Images/Explosion/4.png",
				"Resources/Images/Explosion/5.png",
				"Resources/Images/Explosion/6.png",
				"Resources/Images/Explosion/7.png",
				"Resources/Images/Explosion/8.png",
				"Resources/Images/Explosion/9.png",
				"Resources/Images/Explosion/10.png",
				"Resources/Images/Explosion/11.png",
				"Resources/Images/Explosion/12.png",
				"Resources/Images/Explosion/13.png",
				"Resources/Images/Explosion/14.png",
				"Resources/Images/Explosion/15.png",
			]),

			"Absorption": Sprite([
				"Resources/Images/Absorption/1.png",
				"Resources/Images/Absorption/2.png",
				"Resources/Images/Absorption/3.png",
				"Resources/Images/Absorption/4.png",
				"Resources/Images/Absorption/5.png",
				"Resources/Images/Absorption/6.png",
				"Resources/Images/Absorption/7.png",
				"Resources/Images/Absorption/8.png",
				"Resources/Images/Absorption/9.png",
			]),

		}

		self._sprites["Small Shield"] = self._sprites["Shield"].GetScaledCopy(Vector(80, 80))
		self._sprites["Small Explosion"] = self._sprites["Explosion"].GetScaledCopy(Vector(100, 100))
		self._sprites["Very Small Explosion"] = self._sprites["Explosion"].GetScaledCopy(Vector(15, 15))

		self._sounds = {

			"Bomb"       : Sound("Resources/Sounds/Bomb.ogg"       , range( 1, 3)),
			"Bullet"     : Sound("Resources/Sounds/Bullet.ogg"     , range( 3, 17)),
			"Destruction": Sound("Resources/Sounds/Destruction.ogg", range(18, 19)),
			"Explosion"  : Sound("Resources/Sounds/Explosion.ogg"  , range(20, 21)),
			"Shield"     : Sound("Resources/Sounds/Shield.ogg"     , range(22, 24)),
			"Absorption" : Sound("Resources/Sounds/Absorption.ogg" , range(25, 26)),

		}

		mixer.music.load("Resources/Sounds/Ambience.ogg")

	def GetFont(self, identifier):

		return self._fonts[identifier]

	def GetBackground(self, identifier):

		return self._backgrounds[identifier]

	def GetSprite(self, identifier):

		return self._sprites[identifier]

	def GetSound(self, identifier):

		return self._sounds[identifier]

##
#
# Utilities.
#
##

def LoadBackground(path):

	return transform.smoothscale(image.load(path), tuple(GetScreenDimensions())).convert_alpha()