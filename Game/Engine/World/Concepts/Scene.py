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

from Engine.Core.Resources import Resources
from Engine.Utilities.General import Blit, GetScreen
from Engine.World.Concepts.Node import Node
from Engine.World.Concepts.Widget import Widget
from Engine.World.Utilities.Timed import Timed

##
#
# The main class.
#
##

class Scene(Timed):

	def __init__(self, background):

		super().__init__()

		self._background = background

		self._nodes = []
		self._widgets = []

		self._nextScene = self

	def Append(self, node):

		if isinstance(node, Widget):

			self._widgets.append(node)

		elif isinstance(node, Node):

			self._nodes.append(node)
			self._nodes.sort(key = lambda x: x._zIndex)

	def React(self, events, keys):

		pass

	def Update(self, milisecondsPassed):

		self.UpdateTimers(milisecondsPassed)

		[node.Update(milisecondsPassed) for node in self._nodes]
		[widget.Update(milisecondsPassed) for widget in self._widgets]

	def Render(self):

		Blit(GetScreen(), Resources().GetBackground(self._background))

		[node.Render() for node in self._nodes]
		[widget.Render() for widget in self._widgets]

	def Execute(self, events, keys, milisecondsPassed):

		self.React(events, keys)
		self.Update(milisecondsPassed)
		self.Render()

	def Show(self):

		pass