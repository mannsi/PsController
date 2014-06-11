__author__ = 'mannsi'

from ..DeviceResponse import DeviceResponse
from ..Commands import BaseCommand


class CustomLoggerInterface:
    def log_sending(self, command: BaseCommand, data, serial):
        raise NotImplementedError()

    def log_receiving(self, device_response: DeviceResponse):
        raise NotImplementedError()

    def log_error(self, error_message: str):
        raise NotImplementedError()

    def log_info(self, info_message: str):
        raise NotImplementedError()