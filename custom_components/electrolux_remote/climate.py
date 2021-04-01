"""
Adds Support for Electrolux Convector

Configuration for this platform:
climate:
  - platform: electrolux_remote
    name: Electrolux Convector
    username: phone
    password: 123456
"""

import logging
import voluptuous as vol

from .device_convector2 import Convector2
from .rusclimatapi import RusclimatApi

import homeassistant.helpers.config_validation as cv

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.components.climate import ClimateEntity, PLATFORM_SCHEMA
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
    CONF_USERNAME,
    CONF_PASSWORD,
    TEMP_CELSIUS,
    PRECISION_WHOLE,
)

from .enum import *
from .const import (
    TYPE_CONVECTOR_2,
    STATE_ON,
    TEMP_COMFORT_MIN,
    TEMP_COMFORT_MAX,
)

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

PRESET_NO_FROST = "no_frost"

HA_PRESET_TO_CONVECTOR = {
    PRESET_COMFORT: WorkMode.MODE_COMFORT,
    PRESET_ECO: WorkMode.MODE_ECO,
    PRESET_NO_FROST: WorkMode.MODE_NO_FROST
}
CONVECTOR_PRESET_TO_HA = {v: k for k, v in HA_PRESET_TO_CONVECTOR.items()}


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices):
    _LOGGER.debug("climate.async_setup_entry")

    data = config_entry.options if config_entry.options != {} else config_entry.data

    _LOGGER.debug("climate.async_setup_entry")

    api = RusclimatApi(
        host=data["host"],
        username=data["username"],
        password=data["password"],
        appcode=data["appcode"],
    )
    json = await api.login()

    devices = []
    for deviceData in json["result"]["device"]:
        _LOGGER.debug(f"device: {deviceData}")

        if deviceData["type"] == TYPE_CONVECTOR_2:
            device = Convector2Climate(Convector2(uid=deviceData["uid"], api=api, data=deviceData))
            devices.append(device)

    _LOGGER.debug(devices)
    async_add_devices(devices)


class Convector2Climate(ClimateEntity):
    """Representation of an Climate."""

    def __init__(self, device: Convector2):
        """Initialize"""
        _LOGGER.debug("climate.Convector2Climate.init")

        self._icon = "mdi:radiator"
        self._device = device
        self._name = "convector_" + device.uid
        self._uid = device.uid
        self._min_temp = TEMP_COMFORT_MIN
        self._max_temp = TEMP_COMFORT_MAX
        self._current_temp = None
        self._heating = False
        self._preset = None
        self._target_temperature = None
        self._available = False

        self._update()

    def _update(self):
        _LOGGER.debug("climate.Convector2Climate.update")

        self._current_temp = self._device.current_temp
        self._heating = self._device.state == STATE_ON
        self._preset = CONVECTOR_PRESET_TO_HA.get(WorkMode(self._device.mode))
        self._available = self._device.online == STATE_ON

        mode = WorkMode(self._device.mode)
        if mode is WorkMode.MODE_COMFORT:
            self._target_temperature = self._device.temp_comfort
        elif mode is WorkMode.MODE_ECO:
            self._target_temperature = self._device.temp_comfort - self._device.delta_eco
        elif mode is WorkMode.MODE_NO_FROST:
            self._target_temperature = self._device.temp_antifrost

    @property
    def hvac_mode(self):
        """Return hvac operation """
        if self._heating:
            return HVAC_MODE_HEAT
        return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes. Need to be a subset of HVAC_MODES. """
        return [HVAC_MODE_HEAT]

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""

        await self._device.set_state(not self._heating)
        self._update()

    @property
    def hvac_action(self):
        """Return the current running hvac operation if supported.  Need to be one of CURRENT_HVAC_*.  """
        if self._heating:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def unique_id(self):
        """Return the unique ID of the binary sensor."""
        return self._uid

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temp

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self._min_temp:
            return self._min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self._max_temp:
            return self._max_temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp."""
        return self._preset

    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        return [PRESET_COMFORT, PRESET_ECO, PRESET_NO_FROST]

    async def async_set_preset_mode(self, preset_mode):
        """Set a new preset mode. If preset_mode is None, then revert to auto."""

        if self._preset == preset_mode:
            return

        await self._device.set_mode(HA_PRESET_TO_CONVECTOR.get(preset_mode, PRESET_COMFORT))
        self._update()

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""

        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return

        await self._device.set_temp_comfort(target_temp)
        self._update()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    @property
    def precision(self):
        return PRECISION_WHOLE

    async def async_update(self):
        await self._device.update()
        self._update()
