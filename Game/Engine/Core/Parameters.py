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

from pathlib import Path
from types import SimpleNamespace

##
#
# Globals.
#
##

Parameters = SimpleNamespace(

	Name = "Star Battles",
	Version = "1.1-D",
	Creator = "Beny Synakiewicz",

	MaximumFrameRate = 120,

	HighscoreFilePath = Path("Highscore.txt"),

	SmallMargin = 4,
	Margin = 12,

	BarHeight = 12,
	ShadowDistance = Vector(3, 3),

	BulletSpeed = 0.300,
	BombSpeed = 0.300,
	EnemySpeed = 0.200,

	BulletEnergyRegeneration = 0.225,
	BombEnergyRegeneration = 0.020,
	ShieldEnergyRegeneration = 0.025,
	ShieldEnergyUsage = 0.050,

)