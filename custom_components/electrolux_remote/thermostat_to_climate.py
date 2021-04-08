"""Thermostat to Climate class"""

import logging

from typing import Any, Dict, List, Optional

from .climate_base import ClimateBase
from .device_thermostat import (
    Thermostat,
    WorkMode,
    TEMP_MIN,
    TEMP_MAX,
)
from .update_coordinator import Coordinator

from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_PRESET_MODE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    PRESET_COMFORT,
    PRESET_ECO,
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_TENTHS,
)


_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

PRESET_CALENDAR = "calendar"
PRESET_MANUAL = "manual"
PRESET_FORSAGE = "forsage"
PRESET_VACATION = "vacation"

SUPPORT_PRESETS = [
    PRESET_CALENDAR,
    PRESET_MANUAL,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_FORSAGE,
    PRESET_VACATION,
]

"""
Supported hvac modes:
- HVAC_MODE_HEAT: Heat to a target temperature (schedule off)
- HVAC_MODE_OFF:  The device runs in a continuous energy savings mode. If
                  configured as one of the supported hvac modes this mode
                  can be used to activate the vacation mode
"""
SUPPORT_MODES = [HVAC_MODE_HEAT]

HA_PRESET_TO_DEVICE = {
    PRESET_CALENDAR: WorkMode.CALENDAR,
    PRESET_MANUAL: WorkMode.MANUAL,
    PRESET_COMFORT: WorkMode.COMFORT,
    PRESET_ECO: WorkMode.ECO,
    PRESET_FORSAGE: WorkMode.FORSAGE,
    PRESET_VACATION: WorkMode.VACATION,
}
DEVICE_PRESET_TO_HA = {v: k for k, v in HA_PRESET_TO_DEVICE.items()}

DEFAULT_NAME = "Electrolux Thermostat"


class Thermostat2Climate(ClimateBase):
    """
    Representation of a climate device
    """

    def __init__(self, uid: str, coordinator: Coordinator, data: Optional[dict] = None):
        """
        Initialize the climate device
        """
        _LOGGER.debug("Thermostat2Climate.init")

        super().__init__(
            coordinator=coordinator,
            uid=uid,
            name=DEFAULT_NAME + uid,
            temp_min=TEMP_MIN,
            temp_max=TEMP_MAX,
            support_flags=SUPPORT_FLAGS,
            support_modes=SUPPORT_MODES,
            support_presets=SUPPORT_PRESETS,
        )

        self.coordinator = coordinator
        self._device = Thermostat(uid, coordinator.api, data)
        self._heating = None
        self._room_temp = None  # комнатная температура
        self._floor_temp = None  # температура пола
        self._sensor_mode = None  # датчик температуры
        self._sensor_type = None  # сопротивление датчика пола
        self._button_lock = None  # блокировка ручного управления
        self._floor_cover_type = None  # тип покрытия пола
        self._open_window = None  # открытое окно
        self._heating_on = None   # нагрев
        self._led_light = None    # использование подсветки
        self._power_per_h = None    # потребление
        self._antifreeze_temp = None
        self._tariff_1 = None
        self._tariff_2 = None
        self._tariff_3 = None

        self._update()

    @staticmethod
    def device_type() -> str:
        return "floor"

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

        await self._device.set_set_temp(target_temperature * 10)
        self._update()

    @property
    def precision(self):
        return PRECISION_TENTHS

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        """
        Return additional Thermostat status details
        The information will be available in Home Assistant for reporting
        or automations based on teh provided information
        """
        return {
            "room_temp": self._room_temp,
            "floor_temp": self._floor_temp,
            "open_window": self._open_window,
            "sensor_mode": self._sensor_mode.name.lower() if self._sensor_mode else None,
            "sensor_type": self._sensor_type.name.lower() if self._sensor_type else None,
            "button_lock": self._button_lock,
            "floor_cover_type": self._floor_cover_type.name.lower() if self._floor_cover_type else None,
            "heating": self._heating_on,
            "led_light": self._led_light,
            "power_per_h": self._power_per_h,
            "antifreeze_temp": self._antifreeze_temp,
            "antifreeze_mode": self._antifreeze_temp > 0,
            "tariff_1": self._tariff_1,
            "tariff_2": self._tariff_2,
            "tariff_3": self._tariff_3,
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
        _LOGGER.debug("Thermostat2Climate.update")

        self._current_temp = self._device.floor_temp
        self._heating = self._device.state
        self._preset = DEVICE_PRESET_TO_HA.get(self._device.mode)
        self._available = self._device.online
        self._target_temperature = self._device.set_temp
        self._name = self._device.room

        self._room_temp = self._device.room_temp
        self._floor_temp = self._device.floor_temp
        self._sensor_mode = self._device.sensor_mode
        self._sensor_type = self._device.sensor_type
        self._button_lock = self._device.button_lock
        self._floor_cover_type = self._device.pol_type
        self._open_window = self._device.open_window
        self._heating_on = self._device.heating_on
        self._led_light = self._device.led_light
        self._power_per_h = self._device.power_per_h
        self._antifreeze_temp = self._device.antifreeze_temp
        self._tariff_1 = self._device.tariff_1
        self._tariff_2 = self._device.tariff_2
        self._tariff_3 = self._device.tariff_3
