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

from Engine.Utilities.Vector import Vector

from enum import auto, Enum

##
#
# The main class.
#
##

class Movement:

	# The constructor.

	def __init__(self, speed, route, startingPosition = None, rotateToDirection = False, enabled = True):

		# Initial configuration.

		self._enabled = enabled

		self._speed = speed

		self._routeType = RouteType.Direction if isinstance(route, Vector) else RouteType.Waypoints
		self._route = route if (RouteType.Waypoints == self._routeType) else route.GetNormalized()

		self._rotateToDirection = rotateToDirection

		# Current state.

		self._currentWaypointIndex = 0

		self._currentPosition = self._route[self._currentWaypointIndex] if (RouteType.Waypoints == self._routeType) else startingPosition
		self._currentRotation = 0

	# Accessors.

	def IsEnabled(self): return self._enabled
	def GetCurrentPosition(self): return self._currentPosition
	def GetCurrentRotation(self): return self._currentRotation

	# Basic operations.

	def Enable(self, enabled):

		self._enabled = enabled

	# Updatings.

	def Update(self, milisecondsPassed):

		if not self._enabled:
			return

		#
		# If we're dealing with waypoints...
		#

		if RouteType.Waypoints == self._routeType:

			# Retrieve relevant waypoints.

			currentWaypoint = self._route[self._currentWaypointIndex]

			nextWaypointIndex = self._currentWaypointIndex + 1
			if nextWaypointIndex == len(self._route):
				nextWaypointIndex = 0

			nextWaypoint = self._route[nextWaypointIndex]

			# Calculate and update current position.

			currentVectorToNextWaypoint = nextWaypoint - self._currentPosition
			currentDirectionVector = currentVectorToNextWaypoint.GetNormalized()

			futurePosition = self._currentPosition + currentDirectionVector * (self._speed * milisecondsPassed)
			futureVectorToNextWaypoint = nextWaypoint - futurePosition

			currentDistanceToNextWaypoint = currentVectorToNextWaypoint.GetLength()
			futureDistanceToNextWaypoint = futureVectorToNextWaypoint.GetLength()

			if futureDistanceToNextWaypoint >= currentDistanceToNextWaypoint:

				self._currentWaypointIndex = nextWaypointIndex
				self._currentPosition = self._route[self._currentWaypointIndex]

				self.Update(milisecondsPassed)

				return

			self._currentPosition = futurePosition

			# Calculate and update current rotation.

			if self._rotateToDirection:

				movementAngle = currentVectorToNextWaypoint.GetAngle()
				self._currentRotation = movementAngle

			else:

				self._currentRotation = 0

		#
		# If we're dealing with direction...
		#

		else:

			self._currentPosition += self._route * (self._speed * milisecondsPassed)

			if self._rotateToDirection:
				self._currentRotation = self._route.GetAngle()

##
#
# Enumerations.
#
##

class RouteType(Enum):

	Direction = auto()
	Waypoints = auto()