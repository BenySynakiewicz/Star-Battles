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

from Engine.Core.State import State
from Engine.Utilities.Direction import Direction
from Engine.World.Nodes.Participants.Saucer import Saucer
from Engine.World.Nodes.Participants.Enemy import Enemy
from Engine.World.Utilities.Timed import Timed

##
#
# The main class.
#
##

class BattleManager(Timed):

	def __init__(self, scene, verticalOffset):

		super().__init__()

		self._scene = scene
		self._verticalOffset = verticalOffset

		self._saucer = None

		self.AppendTimer("LineEnemy")
		self.AppendTimer("Saucer")

	def Update(self, milisecondsPassed):

		self.UpdateTimers(milisecondsPassed)

		# Forget the saucer if it's terminated.

		if self._saucer and self._saucer.IsTerminated():
			self._saucer = None

		# Spawn enemies.

		if self.GetTimer("LineEnemy") // 1000 > 0:
			self._SpawnLineEnemies()

		# Spawn the saucer.

		if self._saucer:

			self.ClearTimer("Saucer")

		elif self.GetTimer("Saucer") // 30000 > 0:

			self._SpawnSaucers()

	def _SpawnLineEnemies(self):

		currentScore = State().GetScoreManager().GetCurrentScore()

		# In the first row...

		self._scene.Append(Enemy(self._scene, self._verticalOffset, 0, Direction.Right))

		# In the sceond row...

		if currentScore >= 100:
			self._scene.Append(Enemy(self._scene, self._verticalOffset, 1, Direction.Left))

		# In the third row...

		if currentScore >= 500:
			self._scene.Append(Enemy(self._scene, self._verticalOffset, 2, Direction.Right))

		# Clear the timer.

		self.ClearTimer("LineEnemy")

	def _SpawnSaucers(self):

		currentScore = State().GetScoreManager().GetCurrentScore()

		self._saucer = Saucer(self._scene, self._verticalOffset, 3.25, Direction.Left)
		self._scene.Append(self._saucer)

		# Clear the timer.

		self.ClearTimer("Saucer")