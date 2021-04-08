"""Convector2 to Climate class"""

import logging

from typing import Any, Dict, List, Optional

from .climate_base import ClimateBase
from .device_convector2 import (
    Convector2,
    WorkMode,
    TEMP_MIN,
    TEMP_MAX,
    TEMP_ANTIFROST_MIN,
    TEMP_ANTIFROST_MAX,
    BRIGHTNESS
)

from .api import ApiInterface

from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_PRESET_MODE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    PRESET_COMFORT,
    PRESET_ECO
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

PRESET_NO_FROST = "no_frost"

SUPPORT_PRESETS = [PRESET_COMFORT, PRESET_ECO, PRESET_NO_FROST]

"""
Supported hvac modes:
- HVAC_MODE_HEAT: Heat to a target temperature (schedule off)
- HVAC_MODE_AUTO: Follow the configured schedule
- HVAC_MODE_OFF:  The device runs in a continuous energy savings mode. If
                  configured as one of the supported hvac modes this mode
                  can be used to activate the vacation mode
"""
SUPPORT_MODES = [HVAC_MODE_HEAT]

HA_PRESET_TO_DEVICE = {
    PRESET_COMFORT: WorkMode.COMFORT,
    PRESET_ECO: WorkMode.ECO,
    PRESET_NO_FROST: WorkMode.NO_FROST
}
DEVICE_PRESET_TO_HA = {v: k for k, v in HA_PRESET_TO_DEVICE.items()}

DEFAULT_NAME = "Electrolux Convector"


class Convector2Climate(ClimateBase):
    """Representation of an Climate."""

    def __init__(self, uid: str, api: ApiInterface, data: dict = None):
        """
        Initialize the climate device
        """
        super().__init__(
            uid=uid,
            name=DEFAULT_NAME + uid,
            temp_min=TEMP_MIN,
            temp_max=TEMP_MAX,
            support_flags=SUPPORT_FLAGS,
            support_modes=SUPPORT_MODES,
            support_presets=SUPPORT_PRESETS,
        )

        self._device = Convector2(uid, api, data)
        self._uid = self._device.uid
        self._heating = False

        self._child_lock = None
        self._sensor_fault = None
        self._window_open = None
        self._mute = None
        self._window_opened = None
        self._calendar_on = None
        self._brightness = None
        self._led_off_auto = None
        self._temp_comfort = None
        self._delta_eco = None
        self._temp_antifrost = None
        self._hours = None
        self._minutes = None
        self._timer = None
        self._power = None
        self._lcd_on = None
        self._time_seconds = None
        self._time_minutes = None
        self._time_hour = None
        self._time_day = None
        self._time_month = None
        self._time_year = None
        self._time_weekday = None
        self._lock = None
        self._preset_monday = None
        self._preset_tuesday = None
        self._preset_wednesday = None
        self._preset_thursday = None
        self._preset_friday = None
        self._preset_saturday = None
        self._preset_sunday = None
        self._preset_day_1 = None
        self._preset_day_2 = None
        self._preset_day_3 = None
        self._preset_day_4 = None
        self._preset_day_5 = None
        self._preset_day_6 = None
        self._preset_day_7 = None
        self._preset_day_8 = None
        self._preset_day_9 = None
        self._preset_day_10 = None
        self._preset_day_11 = None
        self._preset_day_12 = None
        self._preset_day_13 = None
        self._preset_day_14 = None
        self._preset_day_15 = None
        self._preset_day_16 = None
        self._preset_day_17 = None
        self._preset_day_18 = None
        self._preset_day_19 = None
        self._preset_day_20 = None
        self._preset_day_21 = None
        self._preset_day_22 = None
        self._preset_day_23 = None
        self._preset_day_24 = None
        
        self._update()

    @staticmethod
    def device_type() -> str:
        return "convector24"

    @property
    def hvac_mode(self):
        """Return hvac operation """
        if self._heating:
            return HVAC_MODE_HEAT
        return HVAC_MODE_OFF

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        await self._device.set_state(not self._heating)
        self._update()

    @property
    def hvac_action(self) -> Optional[str]:
        """Return the current running hvac operation if supported.  Need to be one of CURRENT_HVAC_*.  """
        if self._heating:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE

    async def async_set_preset_mode(self, preset_mode) -> None:
        """Set a new preset mode. If preset_mode is None, then revert to auto."""

        if self._preset == preset_mode:
            return

        if not preset_mode.lower() in SUPPORT_PRESETS:
            _LOGGER.warning(
                "%s: set preset mode to '%s' is not supported. "
                "Supported preset modes are %s",
                self._name, str(preset_mode.lower()), SUPPORT_PRESETS)
            return None

        await self._device.set_mode(HA_PRESET_TO_DEVICE.get(preset_mode, PRESET_COMFORT))
        self._update()

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""

        target_temperature = kwargs.get(ATTR_TEMPERATURE)
        if target_temperature is None:
            return

        if (target_temperature < self._min_temp or
                target_temperature > self._max_temp):
            _LOGGER.warning(
                "%s: set target temperature to %s°C is not supported. "
                "The temperature can be set between %s°C and %s°C",
                self._name, str(target_temperature),
                self._min_temp, self._max_temp)
            return

        if self._preset == PRESET_NO_FROST:
            await self._device.set_temp_antifrost(target_temperature)
        elif self._preset == PRESET_ECO:
            target_temperature = target_temperature + self._device.delta_eco
            await self._device.set_temp_comfort(target_temperature)
        else:
            await self._device.set_temp_comfort(target_temperature)

        self._update()

    @property
    def precision(self):
        return PRECISION_WHOLE

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        """
        Return additional Thermostat status details
        The information will be available in Home Assistant for reporting
        or automations based on teh provided information
        """
        return {
            "child_lock": self._child_lock,
            "sensor_fault": self._sensor_fault,
            "window_open": self._window_open,
            "mute": self._mute,
            "window_opened": self._window_opened,
            "calendar_on": self._calendar_on,
            "brightness": self._brightness,
            "led_off_auto": self._led_off_auto,
            "temp_comfort": self._temp_comfort,
            "delta_eco": self._delta_eco,
            "temp_antifrost": self._temp_antifrost,
            "hours": self._hours,
            "minutes": self._minutes,
            "timer": self._timer,
            "power": self._power,
            "lcd_on": self._lcd_on,
            "time_seconds": self._time_seconds,
            "time_minutes": self._time_minutes,
            "time_hour": self._time_hour,
            "time_day": self._time_day,
            "time_month": self._time_month,
            "time_year": self._time_year,
            "time_weekday": self._time_weekday,
            "lock": self._lock,
            "preset_monday": self._preset_monday,
            "preset_tuesday": self._preset_tuesday,
            "preset_wednesday": self._preset_wednesday,
            "preset_thursday": self._preset_thursday,
            "preset_friday": self._preset_friday,
            "preset_saturday": self._preset_saturday,
            "preset_sunday": self._preset_sunday,
            "preset_day_1": self._preset_day_1,
            "preset_day_2": self._preset_day_2,
            "preset_day_3": self._preset_day_3,
            "preset_day_4": self._preset_day_4,
            "preset_day_5": self._preset_day_5,
            "preset_day_6": self._preset_day_6,
            "preset_day_7": self._preset_day_7,
            "preset_day_8": self._preset_day_8,
            "preset_day_9": self._preset_day_9,
            "preset_day_10": self._preset_day_10,
            "preset_day_11": self._preset_day_11,
            "preset_day_12": self._preset_day_12,
            "preset_day_13": self._preset_day_13,
            "preset_day_14": self._preset_day_14,
            "preset_day_15": self._preset_day_15,
            "preset_day_16": self._preset_day_16,
            "preset_day_17": self._preset_day_17,
            "preset_day_18": self._preset_day_18,
            "preset_day_19": self._preset_day_19,
            "preset_day_20": self._preset_day_20,
            "preset_day_21": self._preset_day_21,
            "preset_day_22": self._preset_day_22,
            "preset_day_23": self._preset_day_23,
            "preset_day_24": self._preset_day_24,
        }

    async def async_update(self):
        """
        Update local data
        """
        await self._device.update()
        self._update()

    def _update(self):
        """
        Update local data
        """
        _LOGGER.debug("Convector2Climate.update")

        self._current_temp = self._device.current_temp
        self._heating = self._device.state
        self._preset = DEVICE_PRESET_TO_HA.get(self._device.mode)
        self._available = self._device.online
        self._name = self._device.room

        if self._device.mode is WorkMode.COMFORT:
            self._target_temperature = self._device.temp_comfort
            self._min_temp = TEMP_MIN
            self._max_temp = TEMP_MAX
        elif self._device.mode is WorkMode.ECO:
            self._target_temperature = self._device.temp_comfort - self._device.delta_eco
            self._min_temp = TEMP_MIN - self._device.delta_eco
            self._max_temp = TEMP_MAX - self._device.delta_eco
        elif self._device.mode is WorkMode.NO_FROST:
            self._target_temperature = self._device.temp_antifrost
            self._min_temp = TEMP_ANTIFROST_MIN
            self._max_temp = TEMP_ANTIFROST_MAX

        self._child_lock = self._device.child_lock
        self._sensor_fault = self._device.sensor_fault
        self._window_open = self._device.window_open
        self._mute = self._device.mute
        self._window_opened = self._device.window_opened
        self._calendar_on = self._device.calendar_on
        self._brightness = BRIGHTNESS[self._device.brightness]
        self._led_off_auto = self._device.led_off_auto
        self._temp_comfort = self._device.temp_comfort
        self._delta_eco = self._device.delta_eco
        self._temp_antifrost = self._device.temp_antifrost
        self._hours = self._device.hours
        self._minutes = self._device.minutes
        self._timer = self._device.timer
        self._power = self._device.power
        self._lcd_on = self._device._lcd_on
        self._time_seconds = self._device.time_seconds
        self._time_minutes = self._device.time_minutes
        self._time_hour = self._device.time_hour
        self._time_day = self._device.time_day
        self._time_month = self._device.time_month
        self._time_year = self._device.time_year
        self._time_weekday = self._device.time_weekday
        self._lock = self._device.lock
        self._preset_monday = self._device._preset_monday
        self._preset_tuesday = self._device.preset_tuesday
        self._preset_wednesday = self._device.preset_wednesday
        self._preset_thursday = self._device.preset_thursday
        self._preset_friday = self._device.preset_friday
        self._preset_saturday = self._device.preset_saturday
        self._preset_sunday = self._device.preset_sunday
        self._preset_day_1 = self._device.preset_day_1
        self._preset_day_2 = self._device.preset_day_2
        self._preset_day_3 = self._device.preset_day_3
        self._preset_day_4 = self._device.preset_day_4
        self._preset_day_5 = self._device.preset_day_5
        self._preset_day_6 = self._device.preset_day_6
        self._preset_day_7 = self._device.preset_day_7
        self._preset_day_8 = self._device.preset_day_8
        self._preset_day_9 = self._device.preset_day_9
        self._preset_day_10 = self._device.preset_day_10
        self._preset_day_11 = self._device.preset_day_11
        self._preset_day_12 = self._device.preset_day_12
        self._preset_day_13 = self._device.preset_day_13
        self._preset_day_14 = self._device.preset_day_14
        self._preset_day_15 = self._device.preset_day_15
        self._preset_day_16 = self._device.preset_day_16
        self._preset_day_17 = self._device.preset_day_17
        self._preset_day_18 = self._device.preset_day_18
        self._preset_day_19 = self._device.preset_day_19
        self._preset_day_20 = self._device.preset_day_20
        self._preset_day_21 = self._device.preset_day_21
        self._preset_day_22 = self._device.preset_day_22
        self._preset_day_23 = self._device.preset_day_23
        self._preset_day_24 = self._device.preset_day_24
