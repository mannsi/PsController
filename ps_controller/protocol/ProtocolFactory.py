import logging

from ..connection.ConnectionFactory import ConnectionFactory
from .UsbProtocol import UsbProtocol
from ..Constants import Constants


class ProtocolFactory:
    def __init__(self):
        self._usb_protocol = None

    def get_protocol(self, protocol_type):
        connection = ConnectionFactory(
            logger=logging.getLogger(Constants.LOGGER_NAME)).get_connection(connection_type=protocol_type)
        if protocol_type == "usb":
            if self._usb_protocol:
                return self._usb_protocol
            else:
                self._usb_protocol = UsbProtocol(connection)
                return self._usb_protocol