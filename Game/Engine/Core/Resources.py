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

from Engine.Media.Sound import Sound
from Engine.Media.Sprite import Sprite
from Engine.Utilities.Singleton import Singleton
from Engine.Utilities.General import GetScreenDimensions

from pygame import image, font, mixer, transform

##
#
# The main class.
#
##

class Resources(metaclass = Singleton):

	def __init__(self):

		self._fonts = {
			"Title" : font.Font("Resources/Fonts/Roboto Condensed Light.ttf", 96),
			"Big"   : font.Font("Resources/Fonts/Roboto Condensed Light.ttf", 48),
			"Medium": font.Font("Resources/Fonts/Roboto Condensed.ttf"      , 18),
		}

		self._backgrounds = {
			"Background": LoadBackground("Resources/Images/Background.jpeg"),
		}

		self._sprites = {

			"Bullet (Green)": Sprite("Resources/Images/Bullet (Green).png"),
			"Bullet (Red)"  : Sprite("Resources/Images/Bullet (Red).png"  ),
			"Player"        : Sprite("Resources/Images/Player.png"        , True),
			"Enemy"         : Sprite("Resources/Images/Enemy.png"         , True),
			"Bomb"          : Sprite("Resources/Images/Bomb.png"          , True),
			"Shield"        : Sprite("Resources/Images/Shield.png"        ),
			"Small Shield"  : Sprite("Resources/Images/Small Shield.png"  ),
			"Explosion"     : Sprite("Resources/Images/Explosion.png"     ),
			"Gem 1"         : Sprite("Resources/Images/Gem 1.png"         , True),
			"Gem 2"         : Sprite("Resources/Images/Gem 2.png"         , True),
			"Gem 3"         : Sprite("Resources/Images/Gem 3.png"         , True),
			"Gem 4"         : Sprite("Resources/Images/Gem 4.png"         , True),
			"Gem 5"         : Sprite("Resources/Images/Gem 5.png"         , True),

		}

		self._sounds = {

			"Bomb"       : Sound("Resources/Sounds/Bomb.ogg"       , range( 1, 3)),
			"Bullet"     : Sound("Resources/Sounds/Bullet.ogg"     , range( 3, 17)),
			"Destruction": Sound("Resources/Sounds/Destruction.ogg", range(18, 19)),
			"Explosion"  : Sound("Resources/Sounds/Explosion.ogg"  , range(20, 21)),
			"Shield"     : Sound("Resources/Sounds/Shield.ogg"     , range(22, 24)),

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