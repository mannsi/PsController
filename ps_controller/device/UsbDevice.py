import threading

from .BaseDeviceInterface import BaseDeviceInterface
from ps_controller import SerialParser, PsControllerException
from ps_controller.Constants import Constants
from ..utilities.Crc import CrcHelper
from ..DeviceResponse import DeviceResponse
from ..DeviceValues import DeviceValues
from ..connection.BaseConnectionInterface import BaseConnectionInterface
from ..logging.CustomLoggerInterface import CustomLoggerInterface


class UsbDevice(BaseDeviceInterface):
    """Interface to a PS201 usb connected device"""

    def __init__(self, connection, logger):
        """Constructor

        :param connection: A connection to a device
        :type connection: BaseConnectionInterface
        :param logger: Used to log messages
        :type logger: CustomLoggerInterface
        """
        self._connection = connection
        self._logger = logger
        self._transactionLock = threading.Lock()

    def connect(self):
        self._connection.connect()
        return self._connection.connected()

    def disconnect(self):
        self._connection.disconnect()

    def connected(self):
        return self._connection.connected()

    def authentication_errors_on_machine(self):
        return not self._connection.has_available_ports()

    def get_all_values(self):
        response = self._send_to_device(Constants.WRITE_ALL_COMMAND, data='', expect_response=True)
        if response.command != Constants.WRITE_ALL_RESPOND:
            self._logger.log_error(
                "Did not receive expected response with Write all command :" + Constants.WRITE_ALL_RESPOND)
            return DeviceValues()
        return SerialParser.from_all_data_to_device_values(response.data)

    def set_target_voltage(self, voltage):
        if voltage <= 20000:
            self._send_to_device(Constants.SET_VOLTAGE_COMMAND, data=str(voltage))

    def set_target_current(self, current):
        if current <= 1000:
            self._send_to_device(Constants.SET_CURRENT_COMMAND, data=str(current))

    def set_output_on(self, is_on):
        command = Constants.SET_OUTPUT_ON_COMMAND
        self._send_to_device(command, data="1" if is_on else "0")

    def _send_to_device(self, command, data, expect_response=False):
        """Sends command and data to device. Verifies the acknowledge response from device and
            verifies response from device if expect_response is True

        :param command: The command to send to device
        :type command: str
        :param data: Data to send to device
        :type data: str
        :param expect_response: If we expect a response from device aside from Acknowledge
        :type expect_response: bool
        :return: DeviceResponse or None -- None if no expected response, otherwise the device response from the device
        :raise: PsControllerException
        """
        with self._transactionLock:
            serial_data_to_device = SerialParser.to_serial(command, data)
            self._logger.log_sending(serial_data_to_device)
            self._connection.set(serial_data_to_device)

            acknowledgement_response = self._get_response_from_device()
            if not acknowledgement_response:
                raise PsControllerException("Empty acknowledge from device")

            acknowledge_ok = self._verify_acknowledgement(acknowledgement_response)
            if not acknowledge_ok:
                raise PsControllerException("Did not receive acknowledge from device")

            crc_ok = self._verify_crc_code(acknowledgement_response)
            if not crc_ok:
                    raise PsControllerException("Incorrect crc code received in acknowledgement")

            if expect_response:
                response = self._get_response_from_device()
                if not response:
                    raise PsControllerException("Empty response from device")
                crc_ok = self._verify_crc_code(response)
                if not crc_ok:
                    raise PsControllerException("Incorrect crc code received in response")
                return response

    def _get_response_from_device(self):
        """Gets a single response from the connected device.

        :return: DeviceResponse or None -- None if something went wrong, otherwise the device response from the device
        """
        serial_response = self._connection.get()
        device_response = SerialParser.from_serial(serial_response)
        if not device_response:
            return None
        self._logger.log_receiving(device_response.serial_response)
        return device_response

    def _verify_crc_code(self, response):
        """Verifies the correctness of the crc code from the device

        :param response: The response to verify crc code from
        :type response: DeviceResponse
        :return: bool -- If crc code is correct or not
        """
        (error, expected_value, actual_value) = CrcHelper.verify_crc_code(response)
        if error:
            error_message = "Unexpected crc code from device. Got " + actual_value + " but expected " + expected_value
            self._logger.log_error(error_message)
            return False
        return True

    def _verify_acknowledgement(self, acknowledgement_response):
        """Verify that :param acknowledgement_response is an acknowledgement response

        :param acknowledgement_response:
        :type acknowledgement_response: DeviceResponse
        :return: bool -- If acknowledge sign is as expected
        """
        if not acknowledgement_response:
            log_string = "Received no response from device"
            self._logger.log_error(log_string)
            return False
        elif acknowledgement_response.command == Constants.NOT_ACKNOWLEDGE_COMMAND:
            log_string = "Received 'NOT ACKNOWLEDGE' from device."
            self._logger.log_error(log_string)
            return False
        elif acknowledgement_response.command != Constants.ACKNOWLEDGE_COMMAND:
            log_string = ("Received neither 'ACKNOWLEDGE' nor 'NOT ACKNOWLEDGE' from device. "
                          "Received : " + acknowledgement_response.decoded_response + " from device")
            self._logger.log_error(log_string)
            return False
        return True
