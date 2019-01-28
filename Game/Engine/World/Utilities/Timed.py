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

from Engine.Utilities.Timer import Timer

##
#
# The main class.
#
##

class Timed:

	def __init__(self):

		self._timers = {}

	def UpdateTimers(self, change):

		for _, timer in self._timers.items():
			timer.Update(change)

	def AppendTimer(self, name):

		self._timers[name] = Timer()

	def ClearTimer(self, name):

		if name not in self._timers:
			return

		self._timers[name].Clear()

	def GetTimer(self, name):

		if name not in self._timers:
			return None

		return self._timers[name].Get()