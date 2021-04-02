"""Convector2 class (type=convector24)"""

import logging

from enum import IntEnum

from .device_base import Device, State
from .api_interface import ApiInterface

_LOGGER = logging.getLogger(__name__)

DELTA_ECO_DEFAULT = 4

TEMP_MIN = 10
TEMP_MAX = 35

TEMP_ANTIFROST_MIN = 3
TEMP_ANTIFROST_MAX = 7


class Preset(IntEnum):
    PRESET_0 = 0
    PRESET_1 = 1
    PRESET_2 = 2
    PRESET_3 = 3
    PRESET_4 = 4
    PRESET_5 = 5
    PRESET_6 = 6
    PRESET_7 = 7


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
    COMFORT = 0
    ECO = 1
    NO_FROST = 2
    OFF = 3


class Convector2(Device):

    def __init__(self, uid: str, api: ApiInterface, data: dict = None):
        _LOGGER.debug("Convector2.init")

        super().__init__(uid, api)

        self._child_lock = State.OFF.value
        self._sensor_fault = State.OFF.value
        self._window_open = State.OFF.value
        self._mute = State.OFF.value
        self._window_opened = State.OFF.value
        self._calendar_on = State.OFF.value
        self._brightness = BrightnessMode.FULL.value    # яркость дисплея
        self._led_off_auto = LedMode.PERMANENT.value    # автоотключение дисплея
        self._temp_comfort = TEMP_MIN                   # температура для режима комфорт
        self._delta_eco = DELTA_ECO_DEFAULT             # дельта для ночной температуры
        self._temp_antifrost = TEMP_ANTIFROST_MIN       # температура для анти-фрост
        self._mode = WorkMode.COMFORT.value             # режим работы
        self._mode_temp_1 = 0
        self._mode_temp_2 = 0
        self._mode_temp_3 = 0
        # таймер
        self._hours = 0
        self._minutes = 0
        self._timer = State.OFF.value

        self._current_temp = 0
        self._heat_mode = HeatMode.AUTO.value   # режим обогрева: авто или ручной
        self._power = PowerMode.POWER_0.value   # можность обогрева
        self._code = 0
        self._lcd_on = State.ON.value
        # текущие дата и время
        self._time_seconds = 0
        self._time_minutes = 0
        self._time_hour = 0
        self._time_day = 0
        self._time_month = 0
        self._time_year = 0
        self._time_weekday = 0
        # пресеты
        self._preset_monday = Preset.PRESET_0.value
        self._preset_tuesday = Preset.PRESET_0.value
        self._preset_wednesday = Preset.PRESET_0.value
        self._preset_thursday = Preset.PRESET_0.value
        self._preset_friday = Preset.PRESET_0.value
        self._preset_saturday = Preset.PRESET_0.value
        self._preset_sunday = Preset.PRESET_0.value
        self._preset_day_1 = WorkMode.OFF.value
        self._preset_day_2 = WorkMode.OFF.value
        self._preset_day_3 = WorkMode.OFF.value
        self._preset_day_4 = WorkMode.OFF.value
        self._preset_day_5 = WorkMode.OFF.value
        self._preset_day_6 = WorkMode.OFF.value
        self._preset_day_7 = WorkMode.OFF.value
        self._preset_day_8 = WorkMode.OFF.value
        self._preset_day_9 = WorkMode.OFF.value
        self._preset_day_10 = WorkMode.OFF.value
        self._preset_day_11 = WorkMode.OFF.value
        self._preset_day_12 = WorkMode.OFF.value
        self._preset_day_13 = WorkMode.OFF.value
        self._preset_day_14 = WorkMode.OFF.value
        self._preset_day_15 = WorkMode.OFF.value
        self._preset_day_16 = WorkMode.OFF.value
        self._preset_day_17 = WorkMode.OFF.value
        self._preset_day_18 = WorkMode.OFF.value
        self._preset_day_19 = WorkMode.OFF.value
        self._preset_day_20 = WorkMode.OFF.value
        self._preset_day_21 = WorkMode.OFF.value
        self._preset_day_22 = WorkMode.OFF.value
        self._preset_day_23 = WorkMode.OFF.value
        self._preset_day_24 = WorkMode.OFF.value

        self._tempid = None
        self._mac = None
        self._room = None   # название помещения
        self._sort = 0
        self._curr_slot = None
        self._active_slot = None
        self._slop = None
        self._curr_scene = None
        self._curr_scene_id = None
        self._wait_slot = None
        self._curr_slot_dropped = 0
        self._curr_scene_dropped = 0
        self._lock = State.OFF.value    # режим блокировки

        self._from_json(data)

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
        _LOGGER.debug(f"set_mode: {mode.value}")

        if await self._api.set_device_param(self.uid, 'mode', mode.value):
            await self.update()

    async def set_temp_comfort(self, value: int):
        _LOGGER.debug(f"set_temp_comfort: {value}")

        if await self._api.set_device_param(self.uid, 'temp_comfort', value):
            await self.update()


    @property
    def child_lock(self) -> bool:
        return int(self._child_lock) == State.ON.value

    @property
    def window_open(self) -> bool:
        return int(self._window_open) == State.ON.value

    @property
    def window_opened(self) -> bool:
        return int(self._window_opened) == State.ON.value

    @property
    def mute(self) -> bool:
        return int(self._mute) == State.ON.value

    @property
    def calendar_on(self) -> bool:
        return int(self._calendar_on) == State.ON.value

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
    def mode(self) -> WorkMode:
        return WorkMode(int(self._mode))

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
    def sort(self) -> int:
        return int(self._sort)

    @property
    def lock(self) -> bool:
        return int(self._lock) == State.ON.value

    @property
    def room(self) -> str:
        return self._room
