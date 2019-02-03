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
	Version = "1.2-D",
	Creator = "Beny Synakiewicz",

	MaximumFrameRate = 120,

	HighscoreFilePath = Path("Highscore.txt"),

	SmallMargin = 4,
	MediumMargin = 8,
	Margin = 12,

	BarHeight = 8,
	ShadowDistance = Vector(3, 3),

	PlayerSpeed = 8,
	BulletSpeed = 0.300,
	BombSpeed = 0.250,
	EnemySpeed = 0.200,
	BonusSpeed = 0.400,
	CargoSpeed = 0.400,

	EnemyValue = 10,
	CargoValue = 50,

	SmallTrajectoryDeviation = 0.03,
	BigTrajectoryDeviation = 0.06,

	TripleShotBonusProbability = 0.03,
	TwoBombsBonusProbability = 0.06,
	QuickerShieldBonusProbability = 0.02,
	ShootAroundBonusProbability = 0.01,

	BulletEnergyRegeneration = 0.225,
	BombEnergyRegeneration = 0.015,
	ShieldEnergyRegeneration = 0.025,
	ShieldEnergyUsage = 0.050,
	LowerShieldEnergyUsage = 0.025,

)