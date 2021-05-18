"""Smart class (type=smart)"""

import logging

from .base import SwitchDevice
from ..enums import State
from ..devices.smart import Smart
from ..update_coordinator import Coordinator
from ..const import DEVICE_SMART

_LOGGER = logging.getLogger(__name__)


class SmartSwitches:
    def __init__(self, uid: str, coordinator: Coordinator):
        """
        Initialize
        """

        device = Smart()

        self.switches = [
            SwitchDevice(
                uid=uid,
                coordinator=coordinator,
                name=f"Self Clean",
                icon_on="",
                icon_off="",
                device=device,
                param_name="self_clean",
                property_name="self_clean",
                value_on=State.ON.value,
                value_off=State.OFF.value
            ),
        ]

    @staticmethod
    def device_type() -> str:
        return DEVICE_SMART

    def get_sensors(self):
        return self.switches
