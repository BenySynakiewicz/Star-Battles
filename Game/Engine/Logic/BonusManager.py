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

class BonusManager:

	def __init__(self):

		self._tripleShot = False
		self._twoBombs = False
		self._quickerShield = False

	def IsTripleShotEnabled(self):

		return self._tripleShot

	def IsTwoBombsEnabled(self):

		return self._twoBombs

	def IsQuickerShieldEnabled(self):

		return self._quickerShield

	def EnableTripleShot(self):

		self._tripleShot = True
		self._twoBombs = False
		self._quickerShield = False

	def EnableTwoBombs(self):

		self._tripleShot = False
		self._twoBombs = True
		self._quickerShield = False

	def EnableQuickerShield(self):

		self._tripleShot = False
		self._twoBombs = False
		self._quickerShield = True

	def Clear(self):

		self._tripleShot = False
		self._twoBombs = False
		self._quickerShield = False