"""
The Electrolux remote integration.
"""

import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

from .const import DOMAIN, PLATFORMS, HOST_RUSKLIMAT, STARTUP_MESSAGE, CONF_APPCODE
from .api import RusclimatApi

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Electrolux component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    # Store an instance of the "connecting" class that does the work of speaking
    # with your actual devices.
    session = async_get_clientsession(hass)
    hass.data[DOMAIN][entry.entry_id] = RusclimatApi(
        entry.data.get(CONF_HOST),
        entry.data.get(CONF_USERNAME),
        entry.data.get(CONF_USERNAME),
        entry.data.get(CONF_USERNAME),
        session
    )

    for platform in PLATFORMS:
        _LOGGER.info("Added new platform: %s, entry_id: %s", entry.title, entry.entry_id)

        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
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
