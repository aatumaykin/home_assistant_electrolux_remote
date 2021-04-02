"""API interface"""
import abc


class ApiInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def login(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_device_params(self, uid: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def set_device_param(self, uid: str, param: str, value) -> bool:
        raise NotImplementedError
