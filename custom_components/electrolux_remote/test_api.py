"""Test Api"""

import logging

from .api_interface import ApiInterface

_LOGGER = logging.getLogger(__name__)


class TestApi(ApiInterface):
    """ Wrapper class to the Rusclimat API """

    def __init__(self, host: str, username: str, password: str, appcode: str):
        _LOGGER.debug("TestApi.init")

        self.devices = [
            {
                "tempid": "181304",
                "state": "1",
                "error": "0",
                "set_temp": "240",
                "room_temp": "292",
                "set_room_temp": "38",
                "floor_temp": "304",
                "sensor_mode": "0",
                "sensor_type": "2",
                "floor_temp_limit": "450",
                "antifreeze_temp": "0",
                "led_light": "30",
                "heating_on": "0",
                "open_window": "1",
                "button_lock": "1",
                "pol_res_set": "1",
                "pol_type": "1",
                "mode": "1",
                "pol_matrix": {
                    "1": {
                        "1": "240",
                        "2": "210",
                        "3": "210",
                        "4": "210",
                        "5": "210"
                    },
                    "2": {
                        "1": "270",
                        "2": "250",
                        "3": "250",
                        "4": "250",
                        "5": "250"
                    },
                    "3": {
                        "1": "320",
                        "2": "280",
                        "3": "270",
                        "4": "270",
                        "5": "280"
                    },
                    "4": {
                        "1": "50",
                        "2": "50",
                        "3": "50",
                        "4": "50",
                        "5": "50"
                    },
                    "5": {
                        "1": "50",
                        "2": "50",
                        "3": "50",
                        "4": "50",
                        "5": "50"
                    }
                },
                "power_per_h": "0",
                "tariff_1": "0",
                "tariff_2": "0",
                "tariff_3": "0",
                "type": "floor",
                "timezone": "3",
                "hours": "22",
                "minutes": "59",
                "uid": "181304",
                "mac": "set",
                "room": "Ванная",
                "sort": "0",
                "curr_slot": "0",
                "active_slot": "0",
                "slop": "0",
                "curr_scene": "0",
                "curr_scene_id": "0",
                "wait_slot": "0",
                "curr_slot_dropped": "0",
                "curr_scene_dropped": "0",
                "online": "1",
                "set_temp_1": "0",
                "set_temp_0": "240",
                "room_temp_1": "1",
                "room_temp_0": "36",
                "set_room_temp_1": "0",
                "set_room_temp_0": "38",
                "floor_temp_1": "1",
                "floor_temp_0": "48",
                "floor_temp_limit_1": "1",
                "floor_temp_limit_0": "194",
                "antifreeze_temp_1": "0",
                "antifreeze_temp_0": "0"
            },
            {
                "tempid": "181305",
                "state": "0",
                "error": "0",
                "set_temp": "350",
                "room_temp": "258",
                "set_room_temp": "0",
                "floor_temp": "226",
                "sensor_mode": "0",
                "sensor_type": "2",
                "floor_temp_limit": "450",
                "antifreeze_temp": "0",
                "led_light": "30",
                "heating_on": "0",
                "open_window": "1",
                "button_lock": "1",
                "pol_res_set": "1",
                "pol_type": "1",
                "mode": "3",
                "pol_matrix": {
                    "1": {
                        "1": "250",
                        "2": "210",
                        "3": "210",
                        "4": "210",
                        "5": "210"
                    },
                    "2": {
                        "1": "270",
                        "2": "250",
                        "3": "250",
                        "4": "250",
                        "5": "250"
                    },
                    "3": {
                        "1": "350",
                        "2": "280",
                        "3": "270",
                        "4": "270",
                        "5": "280"
                    },
                    "4": {
                        "1": "50",
                        "2": "50",
                        "3": "50",
                        "4": "50",
                        "5": "50"
                    },
                    "5": {
                        "1": "50",
                        "2": "50",
                        "3": "50",
                        "4": "50",
                        "5": "50"
                    }
                },
                "power_per_h": "0",
                "tariff_1": "0",
                "tariff_2": "0",
                "tariff_3": "0",
                "type": "floor",
                "timezone": "3",
                "hours": "22",
                "minutes": "59",
                "uid": "181305",
                "mac": "set",
                "room": "Балкон",
                "sort": "0",
                "curr_slot": "0",
                "active_slot": "0",
                "slop": "0",
                "curr_scene": "0",
                "curr_scene_id": "0",
                "wait_slot": "0",
                "curr_slot_dropped": "0",
                "curr_scene_dropped": "0",
                "set_temp_1": "1",
                "set_temp_0": "94",
                "room_temp_1": "1",
                "room_temp_0": "2",
                "set_room_temp_1": "0",
                "set_room_temp_0": "0",
                "floor_temp_1": "0",
                "floor_temp_0": "226",
                "floor_temp_limit_1": "1",
                "floor_temp_limit_0": "194",
                "antifreeze_temp_1": "0",
                "antifreeze_temp_0": "0",
                "online": "1"
            },
            {'state': '0', 'child_lock': '0', 'sensor_fault': '0', 'window_open': '0', 'mute': '0',
             'window_opened': '0', 'calendar_on': '0', 'brightness': '1', 'led_off_auto': '0', 'temp_comfort': '10',
             'delta_eco': '4', 'temp_antifrost': '7', 'mode': '1', 'mode_temp_1': '0', 'mode_temp_2': '0',
             'mode_temp_3': '0', 'hours': '12', 'minutes': '0', 'timer': '0', 'current_temp': '8', 'heat_mode': '1',
             'power': '1', 'code': '0', 'lcd_on': '1', 'time_seconds': '4', 'time_minutes': '55', 'time_hour': '0',
             'time_day': '1', 'time_month': '4', 'time_year': '21', 'time_weekday': '4', 'preset_monday': '0',
             'preset_tuesday': '0', 'preset_wednesday': '0', 'preset_thursday': '0', 'preset_friday': '0',
             'preset_saturday': '0', 'preset_sunday': '0', 'preset_day_1': '0', 'preset_day_2': '0',
             'preset_day_3': '0', 'preset_day_4': '0', 'preset_day_5': '0', 'preset_day_6': '0', 'preset_day_7': '0',
             'preset_day_8': '2', 'preset_day_9': '2', 'preset_day_10': '2', 'preset_day_11': '2',
             'preset_day_12': '2', 'preset_day_13': '2', 'preset_day_14': '2', 'preset_day_15': '2',
             'preset_day_16': '2', 'preset_day_17': '2', 'preset_day_18': '2', 'preset_day_19': '2',
             'preset_day_20': '2', 'preset_day_21': '2', 'preset_day_22': '2', 'preset_day_23': '2',
             'preset_day_24': '0', 'tempid': '188577', 'uid': '188577', 'mac': 'set', 'room': 'баня', 'sort': '0',
             'type': 'convector24', 'curr_slot': '0', 'active_slot': '0', 'slop': '0', 'curr_scene': '0',
             'curr_scene_id': '0', 'wait_slot': '0', 'curr_slot_dropped': '0', 'curr_scene_dropped': '0',
             'online': '1', 'lock': '0'}
        ]

    async def login(self):
        json = {
            'result': {
                'token': '123456',
                'device': self.devices
            },
            'error_code': '0',
            'error_message': ''
        }

        return json

    async def get_device_params(self, uid: str):
        return self.devices

    async def set_device_param(self, uid: str, param: str, value) -> bool:
        for i, device in enumerate(self.devices):
            if device["uid"] == uid:
                self.devices[i][param] = value

        return True
