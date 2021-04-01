"""Constants of API"""

# request uri
API_LOGIN = "api/userAuth"
API_CHANGE_PASSWORD = "api/userChangePassword"
API_CREATE_CALENDAR = "api/setTimeSlot"
API_DELETE_DEVICE = "api/deleteDevice"
API_DELETE_DEVICE_BY_TEMP_ID = "api/deleteDeviceByTempID"
API_PUT_DEVICE = "api/putDevice"
API_GET_DEVICE_PARAMS = "api/getDeviceParams"
API_SET_DEVICE_PARAMS = "api/setDeviceParams"
API_REGISTRATION = "api/userRegister"
API_REMIND_PASSWORD = "api/userRemindPassword"
API_SEND_CODE = "api/userRegister"
API_UPDATE_CALENDAR_SLOTS = "api/setTimeSlot"

# response code
ERROR_INCORRECT_LOGIN_OR_PASSWORD = "106"
ERROR_INCORRECT_PHONE = "112"               # Слишком короткий номер телефона
ERROR_TOKEN_NOT_FOUND = "121"               # Токен не найден
ERROR_USER_NOT_FOUND = "136"                # Пользователь не найден
ERROR_DEVICE_UNAVAILABLE = "153"            # Ошибка - устройство не в сети или неизвестный тип
