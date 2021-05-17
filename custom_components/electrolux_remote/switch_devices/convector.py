"""Convector class (type=conv)"""

import logging

from .base import SwitchDevice
from ..enums import State
from ..devices.convector import Convector
from ..update_coordinator import Coordinator
from ..const import DEVICE_CONVECTOR

_LOGGER = logging.getLogger(__name__)


class ConvectorSwitches:
    def __init__(self, uid: str, coordinator: Coordinator):
        """
        Initialize
        """

        device = Convector()

        self.switches = [
            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Led",
                icon_on="mdi:theme-light-dark",
                icon_off="mdi:theme-light-dark",
                device=device,
                param_name="led",
                property_name="led",
                value_on=State.OFF.value,
                value_off=State.ON.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Lock",
                icon_on="mdi:lock",
                icon_off="mdi:lock",
                device=device,
                param_name="lock",
                property_name="lock",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Timer",
                icon_on="mdi:timer",
                icon_off="mdi:timer",
                device=device,
                param_name="timer",
                property_name="timer",
                value_on=State.ON.value,
                value_off=State.OFF.value
            )
        ]

    @staticmethod
    def device_type() -> str:
        return DEVICE_CONVECTOR

    def get_sensors(self):
        return self.switches
