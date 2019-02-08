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

from Engine.Utilities.Singleton import Singleton

from Engine.Core.Parameters import Parameters
from Engine.Core.Resources import Resources
from Engine.Utilities.General import TakeScreenshot
from Engine.World.Scenes.TitleScene import TitleScene

from sys import exit

from pygame import(
	display, event, font, key, mixer, mouse, time,
	DOUBLEBUF, FULLSCREEN, HWSURFACE, K_ESCAPE, K_F12, KEYDOWN, QUIT,
)

##
#
# The main class.
#
##

class Game:

	def __init__(self):

		self._InitializeComponents(frequency = 44100, channels = 26)
		self._InitializeWindow(f"{Parameters.Name} (by {Parameters.Creator})")
		self._InitializeResources()

	def Run(self):

		# Intialize the first scene and play the music.

		scene = TitleScene()
		mixer.music.play()

		# Enter the main loop.

		timeSincePreviousFrame = 0
		clock = time.Clock()

		while True:

			events = [x for x in event.get()]
			keys = key.get_pressed()

			for x in events:

				pass

				if (QUIT == x.type) or (KEYDOWN == x.type and K_ESCAPE == x.key):
					exit()

				if (KEYDOWN == x.type and K_F12 == x.key):
					TakeScreenshot()

			scene.Execute(events, keys, timeSincePreviousFrame)

			scene = scene._nextScene
			if not scene:
				scene = TitleScene()

			display.flip()

			timeSincePreviousFrame = clock.tick(Parameters.MaximumFrameRate)

	def _InitializeComponents(self, frequency, channels):

		# Initialize pygame.

		font.init()

		display.init()

		mixer.pre_init(frequency)
		mixer.init()
		mixer.set_num_channels(channels)

	def _InitializeWindow(self, title):

		display.set_mode((0, 0), DOUBLEBUF | FULLSCREEN | HWSURFACE)
		display.set_caption(title)

		mouse.set_visible(False)

	def _InitializeResources(self):

		# Load fonts.

		Resources().LoadFont("Title", "Resources/Fonts/Exo 2 Light.ttf", 96)
		Resources().LoadFont("Big", "Resources/Fonts/Exo 2 Light.ttf", 48)
		Resources().LoadFont("Medium", "Resources/Fonts/Exo 2.ttf", 18)

		# Load backgrounds.

		Resources().LoadBackground("Background", "Resources/Images/Background.jpeg")

		# Load sprites.

		Resources().LoadSprite("Bullet (Green)", "Resources/Images/Bullet (Green).png")
		Resources().LoadSprite("Bullet (Red)", "Resources/Images/Bullet (Red).png")
		Resources().LoadSprite("Shield", "Resources/Images/Shield.png")
		Resources().LoadSprite("Bonus 1", "Resources/Images/Bonus 1/")
		Resources().LoadSprite("Bonus 2", "Resources/Images/Bonus 2/")
		Resources().LoadSprite("Bonus 3", "Resources/Images/Bonus 3/")
		Resources().LoadSprite("Bonus 4", "Resources/Images/Bonus 4/")
		Resources().LoadSprite("Player", "Resources/Images/Player/", shadows = True, framesPerSecond = 6)
		Resources().LoadSprite("Enemy", "Resources/Images/Enemy/", shadows = True, framesPerSecond = 6)
		Resources().LoadSprite("Bomb", "Resources/Images/Bomb/", shadows = True, framesPerSecond = 6)
		Resources().LoadSprite("Explosion", "Resources/Images/Explosion/")
		Resources().LoadSprite("Absorption", "Resources/Images/Absorption/")

		# Load sounds.

		Resources().LoadSound("Bomb", "Resources/Sounds/Bomb.ogg", range( 1,  3))
		Resources().LoadSound("Bullet", "Resources/Sounds/Bullet.ogg", range( 3, 17))
		Resources().LoadSound("Destruction", "Resources/Sounds/Destruction.ogg", range(18, 19))
		Resources().LoadSound("Explosion", "Resources/Sounds/Explosion.ogg", range(20, 21))
		Resources().LoadSound("Shield", "Resources/Sounds/Shield.ogg", range(22, 24))
		Resources().LoadSound("Absorption", "Resources/Sounds/Absorption.ogg", range(25, 26))

		# Load music.

		Resources().LoadMusic("Resources/Sounds/Ambience.ogg")