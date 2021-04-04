"""Thermostat class (type=floor)"""

import logging

from enum import Enum, IntEnum

from .device_base import Device, State
from .api_interface import ApiInterface

_LOGGER = logging.getLogger(__name__)

TEMP_MIN = 0
TEMP_MAX = 40


class WorkMode(IntEnum):
    MANUAL = 0
    ECO = 1
    COMFORT = 2
    FORSAGE = 3
    VACATION = 4
    CALENDAR = 5


class FloorCoverType(IntEnum):
    TILE = 0
    CARPET = 1
    LAMINATE = 2
    LINOLEUM = 3
    PARQUET = 4

class Thermostat(Device):

    def __init__(self, uid: str, api: ApiInterface, data: dict = None):
        _LOGGER.debug("Thermostat.init")

        super().__init__(uid, api)

        self._error = 0
        self._set_temp = 240
        self._room_temp = 275  # комнатная температура
        self._set_room_temp = 38
        self._floor_temp = 304  # температура пола
        self._sensor_mode = 0
        self._sensor_type = 2
        self._floor_temp_limit = 450
        self._antifreeze_temp = 0
        self._led_light = None
        self._heating_on = None
        self._open_window = None
        self._button_lock = State.OFF   # блокировка кнопки
        self._pol_res_set = State.OFF   # в приложении переменная называется firstSetUp
        self._pol_type = FloorCoverType.TILE.value  # тип покрытия пола
        self._mode = WorkMode.COMFORT.value  # режим работы
        self._pol_matrix = {}
        self._power_per_h = 0
        self._tariff_1 = 0
        self._tariff_2 = 0
        self._tariff_3 = 0
        self._timezone = 0
        self._hours = 0
        self._minutes = 0
        self._mac = None
        self._room = None   # название помещения
        self._sort = 0
        self._curr_slot = 0
        self._active_slot = 0
        self._slop = 0
        self._curr_scene = 0
        self._curr_scene_id = 0
        self._wait_slot = 0
        self._curr_slot_dropped = 0
        self._curr_scene_dropped = 0
        self._set_temp_1 = 0
        self._set_temp_0 = 240
        self._room_temp_1 = 1
        self._room_temp_0 = 19
        self._set_room_temp_1 = 0
        self._set_room_temp_0 = 38
        self._floor_temp_1 = 1
        self._floor_temp_0 = 48
        self._floor_temp_limit_1 = 1
        self._floor_temp_limit_0 = 194
        self._antifreeze_temp_1 = 0
        self._antifreeze_temp_0 = 0

        self._from_json(data)

    async def set_mode(self, mode: WorkMode):
        _LOGGER.debug(f"set_mode: {mode.value}")

        if await self._api.set_device_param(self.uid, 'mode', mode.value):
            await self.update()

    async def set_temp(self, value: int):
        _LOGGER.debug(f"set_temp: {value}")

        if await self._api.set_device_param(self.uid, 'set_temp', value):
            await self.update()

    @property
    def window_open(self) -> bool:
        return int(self._open_window) == State.ON.value

    @property
    def button_lock(self) -> bool:
        return int(self._button_lock) == State.ON.value

    @property
    def room(self) -> str:
        return self._room

    @property
    def mode(self) -> WorkMode:
        return WorkMode(int(self._mode))

    @property
    def pol_type(self) -> FloorCoverType:
        return FloorCoverType(int(self._pol_type))

    @property
    def room_temp(self) -> float:
        return float(self._room_temp) / 10

    @property
    def floor_temp(self) -> float:
        return float(self._floor_temp) / 10

    @property
    def floor_temp_0(self) -> float:
        return float(self._floor_temp_0) / 10
