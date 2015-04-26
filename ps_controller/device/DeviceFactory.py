from ..connection.ConnectionFactory import ConnectionFactory
from .UsbDevice import UsbDevice
from ..logging.CustomLogger import CustomLogger
from ..logging.CustomLoggerInterface import CustomLoggerInterface
from ps_controller.device import BaseDeviceInterface
import logging


class DeviceFactory:
    """Generates device interfaces"""
    def __init__(self):
        self._usb_device = None

    def get_device(self, device_type, logger=None):
        """Gets a device of device type

        :param device_type: Which device type to get
        :type device_type: str
        :param logger: Logger used for logging messages
        :type logger: CustomLoggerInterface
        :return: BaseDeviceInterface -- Returns the device
        """
        if not logger:
            logger = CustomLogger(logging.DEBUG)
        connection = ConnectionFactory(logger).get_connection(connection_type=device_type)
        if device_type == "usb":
            if self._usb_device:
                return self._usb_device
            else:
                self._usb_device = UsbDevice(connection, logger)
                return self._usb_device