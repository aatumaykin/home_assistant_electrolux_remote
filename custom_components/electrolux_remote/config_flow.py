"""Config flow for Electrolux integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

from .const import DOMAIN, HOST_RUSKLIMAT, APPCODE_ELECTROLUX
from .exception import InvalidHost, CannotConnect, InvalidAuth, UserNotFound
from .rusclimatapi import RusclimatApi

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Optional(CONF_HOST, default=HOST_RUSKLIMAT): str,
    vol.Optional("appcode", default=APPCODE_ELECTROLUX): str,
})


async def validate_input(hass: core.HomeAssistant, data: dict):
    """Validate the user input allows us to connect."""

    if len(data["host"]) < 3:
        raise InvalidHost

    api = RusclimatApi(
        host=data["host"],
        username=data["username"],
        password=data["password"],
        appcode=data["appcode"],
    )
    await api.login()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow."""

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except (InvalidAuth, UserNotFound):
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title="Electrolux remote", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )



