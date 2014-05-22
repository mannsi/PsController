import logging
import threading

from .BaseProtocolInterface import BaseProtocolInterface
from ..data_mapping.UsbDataMapping import UsbDataMapping
from ..Constants import *
from ..utilities.Crc import Crc16


class UsbProtocol(BaseProtocolInterface):
    def __init__(self, connection):
        super(UsbProtocol, self).__init__(connection)
        self._transactionLock = threading.Lock()

    def connect(self):
        return self._connection.connected()

    def connected(self):
        return self._connection.connected()

    def get_all_values(self):
        response = self._send_to_device(WRITE_ALL)
        return response.data

    def set_target_voltage(self, voltage):
        self._send_to_device(READ_TARGET_VOLTAGE)

    def set_target_current(self, current):
        self._send_to_device(READ_TARGET_CURRENT)

    def set_device_is_on(self, is_on):
        if is_on:
            command = TURN_ON_OUTPUT
        else:
            command = TURN_OFF_OUTPUT
        self._send_to_device(command)

    def _send_to_device(self, command, data=''):
        with self._transactionLock:
            serial_data_to_device = UsbDataMapping.to_serial(command, data)
            self._connection.set(serial_data_to_device)
            acknowledgement = self._get_response_from_device()
            UsbProtocol._verify_acknowledgement(acknowledgement, command, data='')
            response = self._get_response_from_device()
        UsbProtocol._verify_response(response, command, data='')
        return response

    def _get_response_from_device(self):
        serial_response = self._connection.get()
        return UsbDataMapping.from_serial(serial_response)

    @classmethod
    def _verify_crc_code(cls, response, command, data):
        """
        Take data from the responses and create crc code like I was sending them
        to the device. Then compare the generated crc code with the crc code from device
        """
        expected_crc_code = Crc16.create(response.command, response.rawData)
        if response.crc != expected_crc_code:
            error_text = "Unexpected crc code from device. Got ", response.crc, " but expected ", expected_crc_code
            cls._log_transmission_error(error_text, command, data, response)

    @classmethod
    def _verify_response(cls, response, command, data):
        cls._verify_crc_code(response, command, data)

    @classmethod
    def _verify_acknowledgement(cls, acknowledgement_response, command, data):
        if not acknowledgement_response:
            cls._log_sending_data_as_error(command, data)
            log_string = "No response from device when sending '" + cls._readable_command(command) + "'"
            logging.getLogger(LOGGER_NAME).error(log_string)
        elif acknowledgement_response.command == NOT_ACKNOWLEDGE:
            log_string = "Received 'NOT ACKNOWLEDGE' from device." \
                         "Command sent to device: '" + cls._readable_command(command) + "'"
            cls._log_transmission_error(log_string, command, data, acknowledgement_response)
        elif acknowledgement_response.command != ACKNOWLEDGE:
            log_string = "Received neither 'ACKNOWLEDGE' nor 'NOT ACKNOWLEDGE' from device. " \
                         "Command sent to device: '" + cls._readable_command(command) + "'"
            cls._log_transmission_error(log_string, command, data, acknowledgement_response)
        else:
            cls._verify_crc_code(acknowledgement_response, command, data)
        cls._verify_response(acknowledgement_response, command, data)

    @classmethod
    def _log_transmission_error(cls, error_message, sending_command, sending_data, response):
        logging.getLogger(LOGGER_NAME).error(error_message)
        cls._log_sending_data_as_error(sending_command, sending_data)
        cls._log_receiving_device_data(response)

    @classmethod
    def _log_sending_data_as_error(cls, command, data):
        log_string = "Command " + cls._readable_command(command) + " sent to device with data " + data
        logging.getLogger(LOGGER_NAME).error(log_string)

    @staticmethod
    def _log_receiving_device_data(device_response):
        logging.getLogger(LOGGER_NAME).error("Data received from device: %s" % ''.join(device_response.readableSerial))

    @staticmethod
    def _readable_command(command):
        if command == WRITE_OUTPUT_VOLTAGE:
            return "Write output voltage"
        elif command == WRITE_OUTPUT_CURRENT:
            return "Write output current"
        elif command == WRITE_INPUT_VOLTAGE:
            return "Write input voltage"
        elif command == WRITE_PRE_REGULATOR_VOLTAGE:
            return "Write pre req voltage"
        elif command == WRITE_ALL:
            return "Write all"
        elif command == WRITE_IS_OUTPUT_ON:
            return "Write is output on"
        elif command == WRITE_TARGET_VOLTAGE:
            return "Write target voltage"
        elif command == WRITE_TARGET_CURRENT:
            return "Write target current"
        elif command == READ_TARGET_VOLTAGE:
            return "Read target voltage"
        elif command == READ_TARGET_CURRENT:
            return "Read target current"
        elif command == TURN_ON_OUTPUT:
            return "Turn output on"
        elif command == TURN_OFF_OUTPUT:
            return "Turn output off"
        elif command == START_STREAM:
            return "Start stream"
        elif command == STOP_STREAM:
            return "Stop stream"
        elif command == ACKNOWLEDGE:
            return "ACKNOWLEDGE"
        elif command == NOT_ACKNOWLEDGE:
            return "NOT_ACKNOWLEDGE"