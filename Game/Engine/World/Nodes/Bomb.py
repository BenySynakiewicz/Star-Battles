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
from Engine.Core.Resources import Resources
from Engine.Utilities.General import GetScreen
from Engine.Utilities.Vector import Vector
from Engine.World.Concepts.MovingNode import MovingNode
from Engine.World.Utilities.Positioning import AtSameCenter

##
#
# The main class.
#
##

class Bomb(MovingNode):

	def __init__(self, scene):

		super().__init__(scene, "Bomb", Vector(0, -Parameters.BombSpeed))

		Resources().GetSound("Bomb").Play()

		self._exploded = False

	def Explode(self):

		if self._exploded:
			return

		self.StopMoving()

		self.ReplaceSprite("Explosion", False)
		Resources().GetSound("Explosion").Play()

		self.AppendTimer("Explosion")
		self._exploded = True

	# Inherited methods.

	def Update(self, milisecondsPassed):

		super().Update(milisecondsPassed)

		if self._exploded and self._sprite.IsFinished():
			self.Terminate()

	def Render(self):

		super().Render()

		if not self._exploded:
			Resources().GetSprite("Small Shield").Blit(
				0,
				GetScreen(),
				AtSameCenter(self.GetPosition(), self.GetDimensions(), Resources().GetSprite("Small Shield").GetDimensions()),
			)

	def OnCollision(self, node):

		if "Bullet" == type(node).__name__:
			return

		self.Explode()