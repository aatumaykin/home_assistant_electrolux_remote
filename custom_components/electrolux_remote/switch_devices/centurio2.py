"""Centurio IQ 2.0 class (type=centurio2)"""

import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.switch import SwitchEntity, ENTITY_ID_FORMAT
from homeassistant.helpers.entity import async_generate_entity_id

from .base import SwitchDevice
from ..enums import State
from ..devices.centurio2 import Centurio2, WaterMode
from ..update_coordinator import Coordinator
from ..const import DEVICE_CENTURIO2

_LOGGER = logging.getLogger(__name__)


class Centurio2Switches:
    def __init__(self, uid: str, coordinator: Coordinator):
        """
        Initialize
        """

        device = Centurio2()

        self.switches = [
            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Bacteria stop system",
                icon_on="mdi:alien",
                icon_off="mdi:alien-outline",
                device=device,
                param_name="self_clean",
                property_name="self_clean",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Economy pause",
                icon_on="",
                icon_off="",
                device=device,
                param_name="economy_pause",
                property_name="economy_pause",
                value_on=State.OFF.value,
                value_off=State.ON.value
            ),

            Timer(
                uid=uid,
                coordinator=coordinator,
                name=f"Timer",
                device=device,
            )
        ]

    @staticmethod
    def device_type() -> str:
        return DEVICE_CENTURIO2

    def get_sensors(self):
        return self.switches


class Timer(CoordinatorEntity, SwitchEntity):
    def __init__(
        self,
        uid: str,
        name: str,
        coordinator: Coordinator,
        device
    ):
        """
        Initialize
        """
        self.coordinator = coordinator

        super().__init__(coordinator)

        self._uid = uid
        self._name = f"{name} {uid}"
        self._device = device

        self.entity_id = async_generate_entity_id(
            f"{ENTITY_ID_FORMAT}", self._name, current_ids=[uid]
        )

        coordinator.async_add_listener(self._update)
        self._update()

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:timer"

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self._device.timer

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        if self._device.timer:
            return

        params = {"timer": State.ON.value, "mode": WaterMode.OFF.value}

        result = await self.coordinator.api.set_device_params(self._uid, params)

        if result:
            self._update_coordinator_data(params)

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        if not self._device.timer:
            return

        params = {"timer": State.OFF.value, "mode": WaterMode.I.value}

        result = await self.coordinator.api.set_device_params(self._uid, params)

        if result:
            self._update_coordinator_data(params)

    async def async_toggle(self) -> None:
        """Turn the entity off."""
        if self._device.timer:
            params = {"timer": State.OFF.value, "mode": WaterMode.I.value}
        else:
            params = {"timer": State.ON.value, "mode": WaterMode.OFF.value}

        result = await self.coordinator.api.set_device_params(self._uid, params)

        if result:
            self._update_coordinator_data(params)

    def _update(self) -> None:
        """
        Update local data
        """
        for data in self.coordinator.data:
            if data["uid"] == self._uid:
                self._device.from_json(data)

    def _update_coordinator_data(self, params: dict) -> None:
        """Update data in coordinator"""
        devices = self.coordinator.data

        for index, device in enumerate(devices):
            if device["uid"] == self._uid:
                for param in params:
                    devices[index][param] = params[param]

        self.coordinator.async_set_updated_data(devices)
        self._update()
