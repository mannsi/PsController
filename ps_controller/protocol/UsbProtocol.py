import logging
import threading

from .BaseProtocolInterface import BaseProtocolInterface
from ..data_mapping.UsbDataMapping import UsbDataMapping
from ..Constants import Constants
from ..utilities.Crc import Crc16
from ..DeviceResponse import DeviceResponse
from ..Commands import *


class UsbProtocol(BaseProtocolInterface):
    def __init__(self, connection):
        """
        Parameters
        ----------
        Connection : BaseConnectionInterface object
        """
        super(UsbProtocol, self).__init__(connection)
        self._transactionLock = threading.Lock()

    def connect(self):
        self._connection.connect()
        return self._connection.connected()

    def disconnect(self):
        self._connection.disconnect()

    def connected(self):
        return self._connection.connected()

    def get_all_values(self):
        response = self._send_to_device(WriteAllValuesCommand(), expect_response=True, data='')
        return UsbDataMapping.from_data_to_device_values(response.data)

    def set_target_voltage(self, voltage):
        self._send_to_device(ReadTargetVoltageCommand(), expect_response=False, data=voltage)

    def set_target_current(self, current):
        self._send_to_device(ReadTargetCurrentCommand(), expect_response=False, data=current)

    def set_device_is_on(self, is_on):
        if is_on:
            command = TurnOnOutputCommand()
        else:
            command = TurnOffOutputCommand()
        self._send_to_device(command, expect_response=False, data='')

    def _send_to_device(self, command: BaseCommand, expect_response: bool, data) -> DeviceResponse:
        with self._transactionLock:
            serial_data_to_device = UsbDataMapping.to_serial(command, data)
            self._connection.set(serial_data_to_device)
            acknowledgement = self._get_response_from_device()
            UsbProtocol._verify_acknowledgement(acknowledgement, command, data='')
            if expect_response:
                response = self._get_response_from_device()
                UsbProtocol._verify_response(response, command, data='')
                return response

    def _get_response_from_device(self) -> DeviceResponse:
        serial_response = self._connection.get()
        return UsbDataMapping.from_serial(serial_response)

    @classmethod
    def _verify_crc_code(cls, response: DeviceResponse, command: BaseCommand, data):
        crc_return_value = Crc16._verify_crc_code(response)
        if crc_return_value:
            error_message = ("Unexpected crc code from device. Got " +
                             crc_return_value[0] + " but expected " + crc_return_value[1])
            cls._log_transmission_error(error_message, command, data, response)

    @classmethod
    def _verify_response(cls, response: DeviceResponse, command: BaseCommand, data):
        cls._verify_crc_code(response, command, data)

    @classmethod
    def _verify_acknowledgement(cls, acknowledgement_response: DeviceResponse, command: BaseCommand, data):
        if not acknowledgement_response:
            cls._log_sending_data_as_error(command, data)
            log_string = "No response from device when sending '" + command.readable() + "'"
            logging.getLogger(Constants.LOGGER_NAME).error(log_string)
        elif acknowledgement_response.command == NotAcknowledgementCommand():
            log_string = "Received 'NOT ACKNOWLEDGE' from device." \
                         "Command sent to device: '" + command.readable() + "'"
            cls._log_transmission_error(log_string, command, data, acknowledgement_response)
        elif acknowledgement_response.command != AcknowledgementCommand():
            log_string = "Received neither 'ACKNOWLEDGE' nor 'NOT ACKNOWLEDGE' from device. " \
                         "Command sent to device: '" + command.readable() + "'"
            cls._log_transmission_error(log_string, command, data, acknowledgement_response)
        else:
            cls._verify_crc_code(acknowledgement_response, command, data)
        cls._verify_response(acknowledgement_response, command, data)

    @classmethod
    def _log_transmission_error(cls, error_message: str, sending_command: BaseCommand,
                                sending_data, response: DeviceResponse):
        logging.getLogger(Constants.LOGGER_NAME).error(error_message)
        cls._log_sending_data_as_error(sending_command, sending_data)
        cls._log_receiving_device_data(response)

    @classmethod
    def _log_sending_data_as_error(cls, command: BaseCommand, data):
        log_string = "Command " + command.readable() + " sent to device with data " + data
        logging.getLogger(Constants.LOGGER_NAME).error(log_string)

    @staticmethod
    def _log_receiving_device_data(device_response: DeviceResponse):
        logging.getLogger(Constants.LOGGER_NAME).error(
            "Data received from device: %s" % ''.join(device_response.readable_serial))