"""Convector class (type=convector24)"""

import logging

from typing import Any, Dict
from enum import IntEnum
from ..enums import State
from ..const import DEVICE_CONVECTOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

TEMP_MIN = 5
TEMP_MAX = 35

DEFAULT_NAME = "Convector"
ICON = "mdi:radiator"


class PowerMode(IntEnum):
    POWER_0 = 0
    POWER_1 = 1
    POWER_2 = 2
    POWER_3 = 3
    POWER_4 = 4
    POWER_5 = 5


class WorkMode(IntEnum):
    COMFORT = 1  # Day
    ECO = 2  # Night
    NO_FROST = 3


class Convector:
    def __init__(self):
        self._state = State.OFF.value
        self._online = State.OFF.value
        self._temp_goal = 24
        self._current_temp = 0
        self._power = PowerMode.POWER_0.value   # мощность обогрева
        self._mode = WorkMode.COMFORT.value             # режим работы
        self._led = State.OFF  # подсветка 0 - вкл, 1 - выкл
        # таймер
        self._hours = 0
        self._minutes = 0
        self._timer = State.OFF.value

        self._room = None   # название помещения
        self._lock = State.OFF.value    # режим блокировки

    def from_json(self, data: dict):
        """Fill self from json data"""
        for key in data:
            setattr(self, f"_{key}", data[key])

    @property
    def current_temp(self) -> float:
        return float(self._current_temp)

    @property
    def mode(self) -> WorkMode:
        return WorkMode(int(self._mode))

    @property
    def temp_goal(self) -> float:
        return float(self._temp_goal)

    @property
    def power(self) -> int:
        return int(self._power)

    @property
    def lock(self) -> bool:
        return int(self._lock) == State.ON.value

    @property
    def room(self) -> str:
        return self._room

    @property
    def state(self) -> bool:
        return int(self._state) == State.ON.value

    @property
    def online(self) -> bool:
        return int(self._online) == State.ON.value

    @property
    def delta_eco(self) -> int:
        return 4

    @property
    def hours(self) -> int:
        return int(self._hours)

    @property
    def minutes(self) -> int:
        return int(self._minutes)

    @property
    def timer(self) -> bool:
        return int(self._timer) == State.ON.value

    @property
    def led(self) -> bool:
        return int(self._led) == State.OFF.value

    @staticmethod
    def device_type() -> str:
        return DEVICE_CONVECTOR

    @staticmethod
    def device_info(data: dict) -> Dict[str, Any]:
        """Device information for entities."""
        return {
            "identifiers": {(DOMAIN, data["uid"])},
            "name": DEFAULT_NAME,
            "suggested_area": data["room"],
            "model": data["type"],
        }
