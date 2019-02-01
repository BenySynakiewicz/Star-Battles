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

from Engine.Core.Parameters import Parameters
from Engine.World.Scenes.TitleScene import TitleScene

from sys import exit

from pygame import(
	display, event, font, key, mixer, mouse, time,
	DOUBLEBUF, FULLSCREEN, HWSURFACE, K_ESCAPE, KEYDOWN, QUIT,
)

##
#
# The start-up routine.
#
##

# Initialize pygame.

font.init()

mixer.pre_init(44100)
mixer.init()
mixer.set_num_channels(26)

# Initialize the screen and the mouse.

display.set_mode((0, 0), DOUBLEBUF | FULLSCREEN | HWSURFACE)
display.set_caption(f"{Parameters.Name} (by {Parameters.Creator})")

mouse.set_visible(False)

# Intialize the first scene and start the music.

scene = TitleScene()
mixer.music.play()

# Enter the main loop.

timeSincePreviousFrame = 0
clock = time.Clock()

while True:

	events = [event for event in event.get()]
	keys = key.get_pressed()

	if any(QUIT == event.type or (KEYDOWN == event.type and K_ESCAPE == event.key) for event in events):
		exit()

	scene.Execute(events, keys, timeSincePreviousFrame)

	scene = scene._nextScene
	if not scene:
		scene = TitleScene()

	display.flip()

	timeSincePreviousFrame = clock.tick(Parameters.MaximumFrameRate)