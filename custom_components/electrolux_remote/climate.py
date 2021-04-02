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

from .convector2_to_climate import Convector2Climate
from .thermostat_to_climate import Thermostat2Climate

from .rusclimatapi import RusclimatApi
from .test_api import TestApi

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


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

        if deviceData["type"] == Convector2Climate.device_type():
            device = Convector2Climate(deviceData["uid"], api, deviceData)
            devices.append(device)

        if deviceData["type"] == Thermostat2Climate.device_type():
            device = Thermostat2Climate(deviceData["uid"], api, deviceData)
            devices.append(device)

    _LOGGER.debug(devices)
    async_add_devices(devices)
