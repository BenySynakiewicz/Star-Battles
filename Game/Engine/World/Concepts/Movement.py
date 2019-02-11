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

	def __init__(self, speed = None, route = None):

		# Initialize the member variables.

		self._routeType = None
		self._route = None

		self._speed = None

		self._currentWaypointIndex = None

		# Initial configuration.

		self.SetRoute(route)
		self.SetSpeed(speed)

	# Accessors.

	def Exists(self):

		if self._routeType == None:
			return False

		if self._route == None:
			return False

		if self._speed  == None:
			return False

		return True

	# Basic operations.

	def Set(self, speed, route):

		self.SetSpeed(speed)
		self.SetRoute(route)

	def SetSpeed(self, speed):

		self._speed = speed

	def SetRoute(self, route):

		self._routeType = RouteType.Direction if isinstance(route, Vector) else RouteType.Waypoints
		self._route = route if (RouteType.Waypoints == self._routeType) else route.GetNormalized()

		self._currentWaypointIndex = 0 if (RouteType.Waypoints == self._routeType) else None

	def Clear(self):

		self._routeType = None
		self._route = None

		self._currentWaypointIndex = None

	# Updatings.

	def Update(self, currentPosition, milisecondsPassed):

		if not self.Exists():
			return

		#
		# Prepare the updated position.
		#

		updatedPosition = Vector(currentPosition.X, currentPosition.Y)

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

			currentVectorToNextWaypoint = nextWaypoint - currentPosition
			currentDirectionVector = currentVectorToNextWaypoint.GetNormalized()

			futurePosition = currentPosition + currentDirectionVector * (self._speed * milisecondsPassed)
			futureVectorToNextWaypoint = nextWaypoint - futurePosition

			currentDistanceToNextWaypoint = currentVectorToNextWaypoint.GetLength()
			futureDistanceToNextWaypoint = futureVectorToNextWaypoint.GetLength()

			if futureDistanceToNextWaypoint >= currentDistanceToNextWaypoint:

				self._currentWaypointIndex = nextWaypointIndex
				updatedPosition = self._route[self._currentWaypointIndex]

				return self.Update(updatedPosition, milisecondsPassed)

			updatedPosition = futurePosition

		#
		# If we're dealing with direction...
		#

		else:

			updatedPosition = currentPosition + self._route * (self._speed * milisecondsPassed)

		#
		# Return the updated position.
		#

		return updatedPosition

##
#
# Enumerations.
#
##

class RouteType(Enum):

	Direction = auto()
	Waypoints = auto()