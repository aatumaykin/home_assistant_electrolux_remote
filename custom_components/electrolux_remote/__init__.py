"""
The Electrolux remote integration.
"""

import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS, HOST_RUSKLIMAT
from .api import RusclimatApi

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Electrolux component."""
    _LOGGER.info("Set up of integration %s", DOMAIN)

    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    _LOGGER.debug("init.async_setup_entry")

    # hass.data[DOMAIN][entry.entry_id] = RusclimatApi(entry.data["host"])

    for platform in PLATFORMS:
        _LOGGER.info("Added new platform: %s, entry_id: %s", entry.title, entry.entry_id)

        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug("init.async_unload_entry")

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        try:
            hass.data[DOMAIN].pop(entry.entry_id)
        except:
            pass

    return unload_ok
