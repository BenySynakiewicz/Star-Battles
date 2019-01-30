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
from Engine.Utilities.Singleton import Singleton

##
#
# The main class.
#
##

class State(metaclass = Singleton):

	def __init__(self):

		self._currentScore: int = 0
		self._highestScore: int = 0

		self.LoadFromFile()

	def LoadFromFile(self):

		if not Parameters.HighscoreFilePath.is_file():
			return

		with open(Parameters.HighscoreFilePath, "r") as file:
			self._highestScore = int(file.read())

	def SaveToFile(self):

		if self._currentScore <= self._highestScore:
			return

		with open(Parameters.HighscoreFilePath, "w") as file:
			file.write(str(self._currentScore))

	def GetCurrentScore(self):

		return self._currentScore

	def GetHighestScore(self):

		return self._highestScore

	def UpdateCurrentScore(self, change):

		self._currentScore += change

		return self._currentScore

	def ClearCurrentScore(self):

		self._currentScore = 0