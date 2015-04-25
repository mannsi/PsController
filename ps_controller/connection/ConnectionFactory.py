from ..connection.UsbConnection import UsbConnection
from ps_controller import SerialParser
from ..logging.CustomLoggerInterface import CustomLoggerInterface

import serial
from ps_controller.Constants import Constants


class ConnectionFactory:
    """ Provides access to connections in the system"""

    def __init__(self, logger):
        """Constructor
        :param logger: logger used by factory and connection
        :type logger: CustomLoggerInterface
        :return: None
        """
        self._usb_connection = None
        self.logger = logger

    def get_connection(self, connection_type):
        """Get an instance of a connection

        :param connection_type: The type of connection to get
        :type connection_type: str
        :return: BaseConnectionInterface -- Connection object
        """
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
        """ Generates a message that can be sent to device for verification.
            Function _device_id_response_function will then check if the response matches the device signature

        :return: bytearray -- The message used for verification
        """
        return SerialParser.to_serial(Constants.HANDSHAKE_COMMAND, data='')

    def _device_id_response_function(self, serial_response, port):
        """Verifies device signature after sending data from function _get_device_message

        :param serial_response: Serial response from device
        :type serial_response: bytearray
        :param port: Serial port being tried
        :type port: str
        :return: bool -- If device is on this port or not
        """
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

    def _get_serial_link(self):
        """Generates an object that implements the serial.Serial interface
        :return: serial.Serial -- An object that can talk directly to a serial device
        """
        return serial.Serial(baudrate=9600, timeout=0.1)