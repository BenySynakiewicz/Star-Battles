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
from Engine.Utilities.General import GetScreen
from Engine.World.Utilities.Timed import Timed

##
#
# The main class.
#
##

class Scene(Timed):

	def __init__(self, background):

		super().__init__()

		self._nodes = []
		self._nextScene = self

		self._background = background

	def AppendNode(self, node):

		self._nodes.append(node)

	def React(self, events, keys):

		pass

	def Update(self, milisecondsPassed):

		self.UpdateTimers(milisecondsPassed)

		for node in self._nodes:
			node.Update(milisecondsPassed)

	def Render(self):

		GetScreen().blit(Resources().GetBackground(self._background), (0, 0))

		for node in self._nodes:
			node.Render()

	def Execute(self, events, keys, milisecondsPassed):

		self.React(events, keys)
		self.Update(milisecondsPassed)
		self.Render()