"""Add support Climate devices"""

import logging

from .climate_devices.convector import ConvectorClimate
from .climate_devices.convector2 import Convector2Climate
from .climate_devices.thermostat import Thermostat2Climate
from .climate_devices.centurio import CenturioClimate
from .climate_devices.centurio2 import Centurio2Climate
from .climate_devices.smart import SmartClimate
from .climate_devices.regency import RegencyClimate

from .const import DOMAIN
from .update_coordinator import Coordinator

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices):
    """
    Setup the climate platform
    """
    coordinator: Coordinator = hass.data[DOMAIN][config_entry.entry_id]

    devices = []

    try:
        for deviceData in coordinator.data:
            device = None

            if deviceData["type"] == ConvectorClimate.device_type():
                device = ConvectorClimate(deviceData["uid"], coordinator)

            if deviceData["type"] == Convector2Climate.device_type():
                device = Convector2Climate(deviceData["uid"], coordinator)

            if deviceData["type"] == Thermostat2Climate.device_type():
                device = Thermostat2Climate(deviceData["uid"], coordinator)

            if deviceData["type"] == CenturioClimate.device_type():
                device = CenturioClimate(deviceData["uid"], coordinator)

            if deviceData["type"] == Centurio2Climate.device_type():
                device = Centurio2Climate(deviceData["uid"], coordinator)

            if deviceData["type"] == SmartClimate.device_type():
                device = SmartClimate(deviceData["uid"], coordinator)

            if deviceData["type"] == RegencyClimate.device_type():
                device = RegencyClimate(deviceData["uid"], coordinator)

            if device is not None:
                _LOGGER.debug(f"add device: {device.name}")
                devices.append(device)

    except Exception as err:
        _LOGGER.error(err)

    if devices:
        async_add_devices(devices)
