"""Convector class (type=conv)"""

import logging

from .device_base import Device
from .api import RusclimatApi
from .const import *
from .enum import *

_LOGGER = logging.getLogger(__name__)


class PowerMode(IntEnum):
    AUTO = 0
    STATE_0 = 1
    STATE_1 = 2
    STATE_2 = 3
    STATE_3 = 4
    STATE_4 = 5
    STATE_5 = 6


MODE_COOL = 0
MODE_DAY = 1
MODE_NIGHT = 2
MODE_UNKNOWN = 3


class Convector(Device):

    def __init__(self, uid: str, api: RusclimatApi, data: dict = None):
        _LOGGER.debug("Convector.init")

        super().__init__(uid, api)
        self._api = api

