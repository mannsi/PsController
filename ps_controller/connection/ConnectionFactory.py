from ..Constants import *
from ..connection.UsbConnection import UsbConnection
from ..data_mapping.UsbDataMapping import UsbDataMapping


class ConnectionFactory:
    def __init__(self, logger):
        self._usb_connection = None
        self.logger = logger

    def get_connection(self, connection_type):
        if connection_type == "usb":
            if self._usb_connection:
                return self._usb_connection
            else:
                self._usb_connection = UsbConnection(
                    baud_rate=9600,
                    timeout=0.1,
                    logger=self.logger,
                    id_message=ConnectionFactory._get_device_message_id(),
                    device_verification_func=self._device_id_response_function)
            return self._usb_connection

    @staticmethod
    def _get_device_message_id():
        """Gives the messages needed to send to device to verify that device is using a given port"""
        return UsbDataMapping.to_serial(HANDSHAKE, data='')

    def _device_id_response_function(self, serial_response):
        """Function used to verify an id response from device, i.e. if the response come from our device or not"""
        try:
            if not serial_response:
                self.logger.info("Did not receive an ACKNOWLEDGE response")
                return False
            response = UsbDataMapping.from_serial(serial_response)
            return response.command == ACKNOWLEDGE
        except:
            self.logger.info("Did not receive an ACKNOWLEDGE response")
            return False