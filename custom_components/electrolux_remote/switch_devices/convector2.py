"""Convector2 class (type=convector24)"""

import logging

from .base import SwitchDevice
from ..enums import State
from ..devices.convector2 import Convector2, BrightnessMode
from ..update_coordinator import Coordinator
from ..const import DEVICE_CONVECTOR24

_LOGGER = logging.getLogger(__name__)


class Convector2Switches:
    def __init__(self, uid: str, coordinator: Coordinator):
        """
        Initialize
        """

        device = Convector2()

        self.switches = [
            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Led off auto",
                icon_on="mdi:theme-light-dark",
                icon_off="mdi:theme-light-dark",
                device=device,
                param_name="led_off_auto",
                property_name="led_off_auto",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Lcd",
                icon_on="mdi:theme-light-dark",
                icon_off="mdi:theme-light-dark",
                device=device,
                param_name="lcd_on",
                property_name="lcd_on",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Brightness",
                icon_on="mdi:theme-light-dark",
                icon_off="mdi:theme-light-dark",
                device=device,
                param_name="brightness",
                property_name="brightness",
                value_on=BrightnessMode.FULL.value,
                value_off=BrightnessMode.HALF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Window Open",
                icon_on="",
                icon_off="",
                device=device,
                param_name="window_open",
                property_name="window_open",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Mute",
                icon_on="",
                icon_off="",
                device=device,
                param_name="mute",
                property_name="mute",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),

            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Lock",
                icon_on="mdi:lock",
                icon_off="mdi:lock",
                device=device,
                param_name="child_lock",
                property_name="child_lock",
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
        return DEVICE_CONVECTOR24

    def get_sensors(self):
        return self.switches
