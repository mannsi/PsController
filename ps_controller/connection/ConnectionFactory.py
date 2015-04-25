from ..connection.UsbConnection import UsbConnection
from ps_controller import SerialParser
from .BaseConnectionInterface import BaseConnectionInterface
from ..logging.CustomLoggerInterface import CustomLoggerInterface

import serial
from ps_controller.Constants import Constants


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
                    device_verification_func=self._device_id_response_function,
                    device_start_end_byte=ord(Constants.START))
            return self._usb_connection

    @staticmethod
    def _get_device_message_id():
        """Gives the messages needed to send to device to verify that device is using a given port"""
        return SerialParser.to_serial(Constants.HANDSHAKE_COMMAND, data='')

    def _device_id_response_function(self, serial_response: bytearray, port: str) -> bool:
        """Function used to verify an id response from device, i.e. if the response come from our device or not"""
        not_ack_string = "Did not receive an ACKNOWLEDGE response on port " + str(port)

        response = SerialParser.from_serial(serial_response)
        if not response:
            self.logger.log(not_ack_string)
            return False

        response.data = port
        return_value = response.command == Constants.ACKNOWLEDGE_COMMAND
        if return_value:
            ack_string = "Received ACKNOWLEDGE response on port " + str(port)
            self.logger.log(ack_string)
        else:
            self.logger.log_receiving(serial_response)
            self.logger.log(not_ack_string)
        return return_value

    def _get_serial_link(self) -> serial.Serial:
        return serial.Serial(baudrate=9600, timeout=0.1)