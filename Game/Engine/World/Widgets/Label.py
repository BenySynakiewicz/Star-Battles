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

from Engine.Utilities.Color import Color
from Engine.Utilities.General import GetDimensions, RenderText
from Engine.World.Concepts.Widget import Widget

##
#
# The main class.
#
##

class Label(Widget):

	# The constructor.

	def __init__(self, scene, text, font, textColor = Color.White):

		super().__init__()

		# Initialize the member variables.

		self._text = text
		self._font = font

		self._textColor = textColor

		# Generate the surface.

		self._GenerateSurface()

	# Accessors.

	def GetText(self): return self._text

	# Operations.

	def SetText(self, text):

		if text != self._text:

			self._text = text
			self._GenerateSurface()

	# Utilities.

	def _GenerateSurface(self):

		if not self._text:

			self.SetSurface(None)

			return

		# Render the text.

		textSurface = RenderText(self._text, self._font, self._textColor)
		textSurfaceDimensions = GetDimensions(textSurface)

		# Set the text surface as the current surface.

		self.SetSurface(textSurface)