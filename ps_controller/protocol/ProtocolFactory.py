from ..connection.ConnectionFactory import ConnectionFactory
from .UsbProtocol import UsbProtocol
from ..logging.CustomLogger import CustomLogger
from ..logging.CustomLoggerInterface import CustomLoggerInterface


class ProtocolFactory:
    def __init__(self, logger: CustomLoggerInterface=None):
        self._usb_protocol = None
        self.logger = logger

    def get_protocol(self, protocol_type):
        if not self.logger:
            self.logger = CustomLogger()
        connection = ConnectionFactory(self.logger).get_connection(connection_type=protocol_type)
        if protocol_type == "usb":
            if self._usb_protocol:
                return self._usb_protocol
            else:
                self._usb_protocol = UsbProtocol(connection, self.logger)
                return self._usb_protocol