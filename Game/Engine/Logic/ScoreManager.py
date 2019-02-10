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
# The main class.
#
##

class ScoreManager:

	def __init__(self):

		self._currentScore = 0
		self._highestScore = 0

	def GetCurrentScore(self):

		return self._currentScore

	def GetHighestScore(self):

		return self._highestScore

	def Update(self, change):

		self._currentScore += change

		return self._currentScore

	def Clear(self):

		self._currentScore = 0
		self._highestScore = 0