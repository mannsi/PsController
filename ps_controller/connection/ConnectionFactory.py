from ..connection.UsbConnection import UsbConnection
from ..data_mapping.UsbDataMapping import UsbDataMapping
from .BaseConnectionInterface import BaseConnectionInterface
from ..Commands import AcknowledgementCommand, HandshakeCommand
from ..logging.CustomLoggerInterface import CustomLoggerInterface

import serial


class ConnectionFactory:
    def __init__(self, logger: CustomLoggerInterface):
        self._usb_connection = None
        self.logger = logger

    def get_connection(self, connection_type) -> BaseConnectionInterface:
        if connection_type == "usb":
            if self._usb_connection:
                return self._usb_connection
            else:
                self._usb_connection = UsbConnection(
                    logger=self.logger,
                    serial_link_generator=self._get_serial_link,
                    id_message=ConnectionFactory._get_device_message_id(),
                    device_verification_func=self._device_id_response_function)
            return self._usb_connection

    @staticmethod
    def _get_device_message_id():
        """Gives the messages needed to send to device to verify that device is using a given port"""
        return UsbDataMapping.to_serial(HandshakeCommand(), data='')

    def _device_id_response_function(self, serial_response: bytearray, port: str) -> bool:
        """Function used to verify an id response from device, i.e. if the response come from our device or not"""
        not_ack_string = "Did not receive an ACKNOWLEDGE response on port " + port
        ack_string = "Received ACKNOWLEDGE response on port " + port
        try:
            if not serial_response:
                self.logger.log_info(not_ack_string)
                return False
            response = UsbDataMapping.from_serial(serial_response)
            response.data = port
            self.logger.log_receiving(response)
            return_value = response.command == AcknowledgementCommand()
            if return_value:
                self.logger.log_info(ack_string)
            else:
                self.logger.log_info(not_ack_string)
            return return_value
        except:
            self.logger.log_info(not_ack_string)
            return False

    def _get_serial_link(self) -> serial.Serial:
        return serial.Serial(baudrate=9600, timeout=0.1)