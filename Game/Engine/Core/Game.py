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

		self._InitializeComponents(frequency = 44100, channels = 28)
		self._InitializeWindow(f"{Parameters.Name} (by {Parameters.Creator})")
		self._InitializeResources()

	def Run(self):

		# Intialize the first scene and play the music.

		scene = TitleScene()
		scene.Show()

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

			if scene._nextScene != scene:
				scene = scene._nextScene or TitleScene()
				scene.Show()

			# scene = scene._nextScene
			# if not scene:
				# scene = TitleScene()
				# scene.Show()

			display.flip()

			timeSincePreviousFrame = clock.tick(Parameters.MaximumFrameRate)

	def _InitializeComponents(self, frequency, channels):

		# Initialize pygame.

		font.init()

		display.init()

		mixer.pre_init(frequency)
		mixer.init()
		mixer.set_num_channels(channels)

		mouse.set_visible(False)

	def _InitializeWindow(self, title):

		display.set_mode((0, 0), DOUBLEBUF | FULLSCREEN | HWSURFACE)
		display.set_caption(title)

	def _InitializeResources(self):

		Resources().Paths.Fonts = "Resources/Fonts"
		Resources().Paths.Sprites = "Resources/Sprites"
		Resources().Paths.Backgrounds = "Resources/Backgrounds"
		Resources().Paths.Sounds = "Resources/Sounds"
		Resources().Paths.Music = "Resources/Music"

		# Load fonts.

		# Resources().LoadFont("Exo 2 Light.ttf")
		# Resources().LoadFont("Exo 2 Light.ttf")
		# Resources().LoadFont("Exo 2.ttf")

		# Load backgrounds.

		# Resources().LoadBackground("Background.jpeg")

		# Load sprites.

		Resources().LoadSprite("Cursor", shadows = False, framesPerSecond = 10)

		Resources().LoadSprite("Bullet (Green).png")
		Resources().LoadSprite("Bullet (Red).png")
		Resources().LoadSprite("Shield.png")
		Resources().LoadSprite("Bonus 1")
		Resources().LoadSprite("Bonus 2")
		Resources().LoadSprite("Bonus 3")
		Resources().LoadSprite("Bonus 4")
		Resources().LoadSprite("Player", shadows = True, framesPerSecond = 6)
		Resources().LoadSprite("Enemy", shadows = True, framesPerSecond = 6)
		Resources().LoadSprite("Saucer.png", shadows = True)
		Resources().LoadSprite("Bomb", shadows = True, framesPerSecond = 6)
		Resources().LoadSprite("Explosion")
		Resources().LoadSprite("Absorption")

		# Load sounds.

		Resources().LoadSound("Bomb.ogg", range( 1,  3))
		Resources().LoadSound("Bullet.ogg", range( 3, 17))
		Resources().LoadSound("Destruction.ogg", range(18, 19))
		Resources().LoadSound("Explosion.ogg", range(20, 21))
		Resources().LoadSound("Shield.ogg", range(22, 24))
		Resources().LoadSound("Absorption.ogg", range(25, 26))
		Resources().LoadSound("Click.ogg", range(27, 28))

		# Load music.

		Resources().LoadMusic("Punch Deck - Catharsis.ogg")
		Resources().LoadMusic("Punch Deck - By Force.ogg")
		Resources().LoadMusic("Punch Deck - Destabilized.ogg")