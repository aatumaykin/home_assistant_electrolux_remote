"""Base device class"""

import logging

from enum import IntEnum
from .api_interface import ApiInterface

_LOGGER = logging.getLogger(__name__)


class State(IntEnum):
    OFF = 0
    ON = 1


class Device:
    def __init__(self, uid: str, api: ApiInterface):
        self._uid = uid
        self._api = api

        self._state = State.OFF.value
        self._online = State.OFF.value

    @property
    def uid(self) -> str:
        return self._uid

    async def set_state(self, value: bool):
        _LOGGER.debug(f"set_state: {value}")

        if await self._api.set_device_param(self.uid, 'state', int(value)):
            await self.update()

    async def update(self):
        for device in await self._api.get_device_params(self.uid):
            if device["uid"] == self.uid:
                self._from_json(device)

    def _from_json(self, data: dict):
        """Fill self from json data"""
        for key in data:
            setattr(self, f"_{key}", data[key])

    @property
    def state(self) -> bool:
        return int(self._state) == State.ON.value

    @property
    def online(self) -> bool:
        return int(self._online) == State.ON.value
