"""Convector2 class"""

import logging

from .device_base import Device
from .rusclimatapi import RusclimatApi
from .const import *
from .enum import *

_LOGGER = logging.getLogger(__name__)


class Convector2(Device):

    def __init__(self, uid: str, api: RusclimatApi, data: dict = None):
        _LOGGER.debug("Convector2.init")

        super().__init__(uid)

        self._api = api
        self._state = STATE_OFF
        self._child_lock = STATE_OFF
        self._sensor_fault = STATE_OFF
        self._window_open = STATE_OFF
        self._mute = STATE_OFF
        self._window_opened = STATE_OFF
        self._calendar_on = STATE_OFF
        self._brightness = BrightnessMode.FULL.value
        self._led_off_auto = LedMode.PERMANENT.value
        self._temp_comfort = TEMP_COMFORT_MIN
        self._delta_eco = DELTA_ECO_DEFAULT
        self._temp_antifrost = TEMP_ANTIFROST_DEFAULT
        self._mode = WorkMode.MODE_COMFORT.value
        self._mode_temp_1 = 0
        self._mode_temp_2 = 0
        self._mode_temp_3 = 0
        self._hours = 0
        self._minutes = 0
        self._timer = STATE_OFF
        self._current_temp = 0
        self._heat_mode = HeatMode.AUTO.value
        self._power = PowerMode.POWER_0.value
        self._code = 0
        self._lcd_on = STATE_ON
        self._time_seconds = 0
        self._time_minutes = 0
        self._time_hour = 0
        self._time_day = 0
        self._time_month = 0
        self._time_year = 0
        self._time_weekday = 0
        self._preset_monday = PRESET_0
        self._preset_tuesday = PRESET_0
        self._preset_wednesday = PRESET_0
        self._preset_thursday = PRESET_0
        self._preset_friday = PRESET_0
        self._preset_saturday = PRESET_0
        self._preset_sunday = PRESET_0
        self._preset_day_1 = WorkMode.MODE_OFF.value
        self._preset_day_2 = WorkMode.MODE_OFF.value
        self._preset_day_3 = WorkMode.MODE_OFF.value
        self._preset_day_4 = WorkMode.MODE_OFF.value
        self._preset_day_5 = WorkMode.MODE_OFF.value
        self._preset_day_6 = WorkMode.MODE_OFF.value
        self._preset_day_7 = WorkMode.MODE_OFF.value
        self._preset_day_8 = WorkMode.MODE_OFF.value
        self._preset_day_9 = WorkMode.MODE_OFF.value
        self._preset_day_10 = WorkMode.MODE_OFF.value
        self._preset_day_11 = WorkMode.MODE_OFF.value
        self._preset_day_12 = WorkMode.MODE_OFF.value
        self._preset_day_13 = WorkMode.MODE_OFF.value
        self._preset_day_14 = WorkMode.MODE_OFF.value
        self._preset_day_15 = WorkMode.MODE_OFF.value
        self._preset_day_16 = WorkMode.MODE_OFF.value
        self._preset_day_17 = WorkMode.MODE_OFF.value
        self._preset_day_18 = WorkMode.MODE_OFF.value
        self._preset_day_19 = WorkMode.MODE_OFF.value
        self._preset_day_20 = WorkMode.MODE_OFF.value
        self._preset_day_21 = WorkMode.MODE_OFF.value
        self._preset_day_22 = WorkMode.MODE_OFF.value
        self._preset_day_23 = WorkMode.MODE_OFF.value
        self._preset_day_24 = WorkMode.MODE_OFF.value
        self._tempid = None
        self._mac = None
        self._room = None
        self._sort = 0
        self._type = TYPE_CONVECTOR_2
        self._curr_slot = None
        self._active_slot = None
        self._slop = None
        self._curr_scene = None
        self._curr_scene_id = None
        self._wait_slot = None
        self._curr_slot_dropped = 0
        self._curr_scene_dropped = 0
        self._online = STATE_OFF
        self._lock = STATE_OFF

        self._from_json(data)

    async def set_state(self, value: bool):
        _LOGGER.debug(f"set_state: {value}")

        if await self._api.set_device_param(self.uid, 'state', int(value)):
            await self.update()

    async def set_child_lock(self, value: bool):
        _LOGGER.debug(f"set_child_lock: {value}")

        if await self._api.set_device_param(self.uid, 'child_lock', int(value)):
            await self.update()

    async def set_window_open(self, value: bool):
        _LOGGER.debug(f"set_window_open: {value}")

        if await self._api.set_device_param(self.uid, 'window_open', int(value)):
            await self.update()

    async def set_mute(self, value: bool):
        _LOGGER.debug(f"set_mute: {value}")

        if await self._api.set_device_param(self.uid, 'mute', int(value)):
            await self.update()

    async def set_brightness(self, mode: BrightnessMode):
        _LOGGER.debug(f"set_brightness: {mode}")

        if await self._api.set_device_param(self.uid, 'brightness', mode.value):
            await self.update()

    async def set_led_off_auto(self, mode: LedMode):
        _LOGGER.debug(f"set_led_off_auto: {mode}")

        if await self._api.set_device_param(self.uid, 'led_off_auto', mode.value):
            await self.update()

    async def set_delta_eco(self, value: int):
        _LOGGER.debug(f"set_delta_eco: {value}")

        if await self._api.set_device_param(self.uid, 'delta_eco', value):
            await self.update()

    async def set_temp_antifrost(self, value: int):
        _LOGGER.debug(f"set_temp_antifrost: {value}")

        if await self._api.set_device_param(self.uid, 'temp_antifrost', value):
            await self.update()

    async def set_heat_mode(self, mode: HeatMode):
        _LOGGER.debug(f"set_heat_mode: {mode}")

        if await self._api.set_device_param(self.uid, 'heat_mode', mode.value):
            await self.update()

    async def set_power(self, mode: PowerMode):
        _LOGGER.debug(f"set_power: {mode}")

        if await self._api.set_device_param(self.uid, 'power', mode.value):
            await self.update()

    async def set_room(self, value: str):
        _LOGGER.debug(f"set_room: {value}")

        if await self._api.set_device_param(self.uid, 'room', value):
            await self.update()

    async def set_lock(self, value: bool):
        _LOGGER.debug(f"set_lock: {value}")

        if await self._api.set_device_param(self.uid, 'lock', int(value)):
            await self.update()

    async def set_mode(self, mode: WorkMode):
        _LOGGER.debug(f"set_mode: {mode}")

        if await self._api.set_device_param(self.uid, 'mode', mode.value):
            await self.update()

    async def set_temp_comfort(self, value: int):
        _LOGGER.debug(f"set_temp_comfort: {value}")

        if await self._api.set_device_param(self.uid, 'temp_comfort', value):
            await self.update()

    @property
    def state(self) -> bool:
        return int(self._state) == STATE_ON

    @property
    def child_lock(self) -> bool:
        return int(self._child_lock) == STATE_ON

    @property
    def window_open(self) -> bool:
        return int(self._window_open) == STATE_ON

    @property
    def window_opened(self) -> bool:
        return int(self._window_opened) == STATE_ON

    @property
    def mute(self) -> bool:
        return int(self._mute) == STATE_ON

    @property
    def calendar_on(self) -> bool:
        return int(self._calendar_on) == STATE_ON

    @property
    def brightness(self) -> int:
        return int(self._brightness)

    @property
    def brightness_half(self) -> bool:
        return int(self._brightness) == BrightnessMode.HALF.value

    @property
    def brightness_full(self) -> bool:
        return int(self._brightness) == BrightnessMode.FULL.value

    @property
    def led_off_auto(self) -> bool:
        return int(self._led_off_auto) == LedMode.AUTO.value

    @property
    def current_temp(self) -> float:
        return float(self._current_temp)

    @property
    def mode(self) -> int:
        return int(self._mode)

    @property
    def temp_comfort(self) -> float:
        return float(self._temp_comfort)

    @property
    def delta_eco(self) -> int:
        return int(self._delta_eco)

    @property
    def temp_antifrost(self) -> int:
        return int(self._temp_antifrost)

    @property
    def hours(self) -> int:
        return int(self._hours)

    @property
    def minutes(self) -> int:
        return int(self._minutes)

    @property
    def timer(self) -> int:
        return int(self._timer)

    @property
    def heat_mode(self) -> int:
        return int(self._heat_mode)

    @property
    def heat_mode_manual(self) -> bool:
        return int(self._heat_mode) == HeatMode.MANUAL.value

    @property
    def heat_mode_auto(self) -> bool:
        return int(self._heat_mode) == HeatMode.AUTO.value

    @property
    def power(self) -> int:
        return int(self._power)

    @property
    def time_seconds(self) -> int:
        return int(self._time_seconds)

    @property
    def time_minutes(self) -> int:
        return int(self._time_minutes)

    @property
    def time_hour(self) -> int:
        return int(self._time_hour)

    @property
    def time_day(self) -> int:
        return int(self._time_day)

    @property
    def time_month(self) -> int:
        return int(self._time_month)

    @property
    def time_year(self) -> int:
        return int(self._time_year)

    @property
    def time_weekday(self) -> int:
        return int(self._time_weekday)

    @property
    def code(self) -> int:
        return int(self._code)

    @property
    def curr_scene_dropped(self) -> int:
        return int(self._curr_scene_dropped)

    @property
    def curr_slot_dropped(self) -> int:
        return int(self._curr_slot_dropped)

    @property
    def curr_scene(self) -> str:
        return self._curr_scene

    @property
    def curr_slot(self) -> int:
        return int(self._curr_slot)

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def online(self) -> bool:
        return int(self._online) == STATE_ON

    @property
    def sort(self) -> int:
        return int(self._sort)

    @property
    def lock(self) -> bool:
        return int(self._lock) == STATE_ON

    async def update(self):
        for device in await self._api.get_device_params(self.uid):
            if device["uid"] == self.uid:
                self._from_json(device)

    def _from_json(self, data: dict):
        """Fill self from json data"""
        for key in data:
            setattr(self, f"_{key}", data[key])

