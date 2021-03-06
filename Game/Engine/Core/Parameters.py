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
	Version = "1.3",
	Creator = "Beny Synakiewicz",

	MaximumFrameRate = 120,

	ScreenshotFilePath = Path("Screenshot.png"),
	HighscoreFilePath = Path("Highscore.txt"),

	SmallMargin = 4,
	MediumMargin = 8,
	Margin = 12,
	HugeMargin = 12 * 12,

	BarHeight = 4,
	ShadowDistance = Vector(3, 3),

	HealthBarHeight = 6,

	PlayerSpeed = 8,
	BulletSpeed = 0.300,
	BombSpeed = 0.250,
	EnemySpeed = 0.200,
	BonusSpeed = 0.400,
	CargoSpeed = 0.400,

	EnemyValue = 10,
	SaucerValue = 100,

	SmallTrajectoryDeviation = 0.03,
	BigTrajectoryDeviation = 0.06,

	TripleShotBonusProbability = 0.030,
	TwoBombsBonusProbability = 0.060,
	QuickerShieldBonusProbability = 0.020,
	ShootAroundBonusProbability = 0.010,
	HealthBonusProbability = 0.020,

	BulletEnergyRegeneration = 0.225,
	BombEnergyRegeneration = 0.015,
	ShieldEnergyRegeneration = 0.025,
	ShieldEnergyUsage = 0.075,
	LowerShieldEnergyUsage = 0.050,

	SmallTextHeight = 20,
	MediumTextHeight = 50,
	BiggishTextHeight = 60,
	BigTextHeight = 90,
	HugeTextHeight = 150,

	ButtonWidth = 300

)