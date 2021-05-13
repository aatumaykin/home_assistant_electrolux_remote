"""Binary sensor."""

import logging

from .const import DOMAIN
from .update_coordinator import Coordinator
from .switch_devices.convector import ConvectorSwitches

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator: Coordinator = hass.data[DOMAIN][config_entry.entry_id]

    try:
        for deviceData in coordinator.data:
            if deviceData["type"] == ConvectorSwitches.device_type():
                async_add_devices(ConvectorSwitches(deviceData["uid"], coordinator).get_sensors())

            # if deviceData["type"] == Convector24Switches.device_type():
            #     devices += Convector24Switches(deviceData["uid"], coordinator).get_sensors()
    except Exception as err:
        _LOGGER.error(err)
