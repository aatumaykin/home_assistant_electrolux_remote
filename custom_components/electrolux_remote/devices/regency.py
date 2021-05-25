"""Regency class (type=regency)"""

import logging

from ..enums import State

_LOGGER = logging.getLogger(__name__)

TEMP_MIN = 35
TEMP_MAX = 75


class Regency:
    def __init__(self):
        self._state = State.OFF.value
        self._online = State.OFF.value
        self._room = None  # название помещения
        self._current_temp = 75
        self._temp_goal = 75
        self._clock_hours = 0
        self._clock_minutes = 0

    def from_json(self, data: dict):
        """Fill self from json data"""
        for key in data:
            setattr(self, f"_{key}", data[key])

    @property
    def room(self) -> str:
        return self._room

    @property
    def online(self) -> bool:
        return int(self._online) == State.ON.value

    @property
    def clock_hours(self) -> int:
        return int(self._clock_hours)

    @property
    def clock_minutes(self) -> int:
        return int(self._clock_minutes)

    @property
    def temp_goal(self) -> int:
        return int(self._temp_goal)

    @property
    def current_temp(self) -> float:
        return float(self._current_temp)

    @property
    def state(self) -> bool:
        return int(self._state) != State.OFF.value
