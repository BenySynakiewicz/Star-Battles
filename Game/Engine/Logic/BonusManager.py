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

	# The constructor.

	def __init__(self):

		self._tripleShot = 0
		self._twoBombs = 0
		self._quickerShield = 0

	# Accessors.

	def IsAnyBonusActive(self):

		return self.IsTripleShotEnabled() or self.IsTwoBombsEnabled() or self.IsQuickerShieldEnabled()

	def GetActiveBonusName(self):

		if self.IsTripleShotEnabled():
			return "TRIPLE SHOT"

		if self.IsTwoBombsEnabled():
			return "TWO BOMBS"

		if self.IsQuickerShieldEnabled():
			return "QUICKER SHIELD"

		return None

	def GetActiveBonusTime(self):

		if self.IsTripleShotEnabled():
			return int(self._tripleShot)

		if self.IsTwoBombsEnabled():
			return int(self._twoBombs)

		if self.IsQuickerShieldEnabled():
			return int(self._quickerShield)

		return None

	def IsTripleShotEnabled(self): return self._tripleShot > 0
	def IsTwoBombsEnabled(self): return self._twoBombs > 0
	def IsQuickerShieldEnabled(self): return self._quickerShield > 0

	# Operations.

	def EnableTripleShot(self, time = 10):

		self._tripleShot += time
		self._twoBombs = 0
		self._quickerShield = 0

	def EnableTwoBombs(self, time = 10):

		self._tripleShot = 0
		self._twoBombs += time
		self._quickerShield = 0

	def EnableQuickerShield(self, time = 10):

		self._tripleShot = 0
		self._twoBombs = 0
		self._quickerShield += time

	def Update(self, milisecondsPassed):

		secondsPassed = milisecondsPassed / 1000

		self._tripleShot -= secondsPassed
		self._twoBombs -= secondsPassed
		self._quickerShield -= secondsPassed

		self._tripleShot = max(self._tripleShot, 0)
		self._twoBombs = max(self._twoBombs, 0)
		self._quickerShield = max(self._quickerShield, 0)

	def Clear(self):

		self._tripleShot = 0
		self._twoBombs = 0
		self._quickerShield = 0