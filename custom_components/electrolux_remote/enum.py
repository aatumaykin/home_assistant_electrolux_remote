from enum import Enum, IntEnum


class BrightnessMode(IntEnum):
    HALF = 0
    FULL = 1


class LedMode(IntEnum):
    PERMANENT = 0
    AUTO = 1


class HeatMode(IntEnum):
    AUTO = 0
    MANUAL = 1


class PowerMode(IntEnum):
    POWER_0 = 0
    POWER_1 = 1
    POWER_2 = 2
    POWER_3 = 3
    POWER_4 = 4
    POWER_5 = 5


class WorkMode(IntEnum):
    MODE_COMFORT = 0
    MODE_ECO = 1
    MODE_NO_FROST = 2
    MODE_OFF = 3
