"""Adds Support for Rusclimat"""

import logging

from aiohttp import ClientSession

from .const import LANG
from .api_const import (
    API_LOGIN,
    API_SET_DEVICE_PARAMS,
    API_GET_DEVICE_PARAMS,
    ERROR_USER_NOT_FOUND,
    ERROR_DEVICE_UNAVAILABLE,
    ERROR_INCORRECT_LOGIN_OR_PASSWORD,
)
from .exception import InvalidAuth, InvalidResponse, UserNotFound, DeviceUnavailable, EnexpectedError
from .api_interface import ApiInterface

_LOGGER = logging.getLogger(__name__)


class RusclimatApi(ApiInterface):
    """ Wrapper class to the Rusclimat API """

    def __init__(self, host: str, username: str, password: str, appcode: str):
        _LOGGER.debug("RusclimatApi.init")

        self._host = host
        self._username = username
        self._password = password
        self._appcode = appcode
        self._token = None
        self.session = None

    def __del__(self):
        _LOGGER.debug('RusclimatApi.destructor')
        # try:
        #     await self.session.close()
        # except Exception:
        #     pass

    def _create_session(self):
        _LOGGER.debug('RusclimatApi._create_session')
        self.session = ClientSession()

    async def _request(self, url: str, payload: dict):
        if self.session is None or self.session.closed:
            self._create_session()

        headers = {
            "lang": LANG,
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.3.1",
        }

        _LOGGER.debug(f"request: {url}")
        _LOGGER.debug(f"payload: {payload}")

        resp = await self.session.post(f"{self._host}/{url}", json=payload, headers=headers)
        json = await resp.json()

        _LOGGER.debug(f"response: {json}")

        if json is None:
            raise InvalidResponse(f"Response error: json is None")

        return json

    async def login(self):
        """Auth on server"""

        payload = {
            "login": self._username,
            "password": self._password,
            "appcode": self._appcode
        }

        json = await self._request(API_LOGIN, payload)

        if json["error_code"] == ERROR_USER_NOT_FOUND:
            raise UserNotFound(json["error_message"])
        elif json["error_code"] == ERROR_INCORRECT_LOGIN_OR_PASSWORD:
            raise InvalidAuth(json["error_message"])
        elif json["error_code"] != "0":
            _LOGGER.exception(f"message: '{json['error_message']}'; code: {json['error_code']}")
            raise InvalidAuth(json["error_message"])

        self._token = json["result"]["token"]

        return json

    async def _update_device_params(self, params: dict):
        if self._token is None:
            await self.login()

        payload = {
            "token": self._token,
            "device": [params]
        }

        json = await self._request(API_SET_DEVICE_PARAMS, payload)

        if json["error_code"] == ERROR_DEVICE_UNAVAILABLE:
            raise DeviceUnavailable(json["error_message"])

        self._check_response_code(json)

        return json

    async def get_device_params(self, uid: str):
        if self._token is None:
            await self.login()

        payload = {
            "token": self._token,
            "uid": [uid]
        }

        json = await self._request(API_GET_DEVICE_PARAMS, payload)

        if json["error_code"] == ERROR_DEVICE_UNAVAILABLE:
            raise DeviceUnavailable(json["error_message"])

        self._check_response_code(json)

        return json["result"]["device"]

    async def set_device_param(self, uid: str, param: str, value) -> bool:
        payload = {
            "uid": uid,
            "params": {
                param: value
            }
        }

        json = await self._update_device_params(payload)

        return self._check_result(json)

    @staticmethod
    def _check_response_code(json):
        if json["error_code"] != "0":
            _LOGGER.exception(f"message: '{json['error_message']}'; code: {json['error_code']}")
            raise EnexpectedError(json["error_message"])

    @staticmethod
    def _check_result(json) -> bool:
        return json["result"] == "1"
