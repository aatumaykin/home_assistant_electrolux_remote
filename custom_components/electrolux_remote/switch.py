"""Binary sensor."""

import logging

from .const import DOMAIN
from .update_coordinator import Coordinator
from .switch_devices.convector import ConvectorSwitches
from .switch_devices.convector2 import Convector2Switches
from .switch_devices.smart import SmartSwitches
from .switch_devices.centurio2 import Centurio2Switches

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices):
    """Setup switch platform."""
    coordinator: Coordinator = hass.data[DOMAIN][config_entry.entry_id]

    try:
        for deviceData in coordinator.data:
            if deviceData["type"] == ConvectorSwitches.device_type():
                devices = ConvectorSwitches(deviceData["uid"], coordinator).get_sensors()
                for device in devices:
                    _LOGGER.debug(f"add device: {device.name}")
                async_add_devices(devices)

            if deviceData["type"] == Convector2Switches.device_type():
                devices = Convector2Switches(deviceData["uid"], coordinator).get_sensors()
                for device in devices:
                    _LOGGER.debug(f"add device: {device.name}")
                async_add_devices(devices)

            if deviceData["type"] == SmartSwitches.device_type():
                devices = SmartSwitches(deviceData["uid"], coordinator).get_sensors()
                for device in devices:
                    _LOGGER.debug(f"add device: {device.name}")
                async_add_devices(devices)

            if deviceData["type"] == Centurio2Switches.device_type():
                devices = Centurio2Switches(deviceData["uid"], coordinator).get_sensors()
                for device in devices:
                    _LOGGER.debug(f"add device: {device.name}")
                async_add_devices(devices)

    except Exception as err:
        _LOGGER.error(err)
