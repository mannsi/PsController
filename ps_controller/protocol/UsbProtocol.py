import threading

from .BaseProtocolInterface import BaseProtocolInterface
from ..data_mapping.UsbDataMapping import UsbDataMapping
from ps_controller import SerialException
from ps_controller.Constants import Constants
from ..utilities.Crc import CrcHelper
from ..DeviceResponse import DeviceResponse
from ..DeviceValues import DeviceValues
from ..connection.BaseConnectionInterface import BaseConnectionInterface
from ..logging.CustomLoggerInterface import CustomLoggerInterface


class UsbProtocol(BaseProtocolInterface):
    def __init__(self, connection: BaseConnectionInterface, logger: CustomLoggerInterface):
        """
        Parameters
        ----------
        Connection : BaseConnectionInterface object
        """
        super(UsbProtocol, self).__init__(connection)
        self._logger = logger
        self._transactionLock = threading.Lock()

    def connect(self):
        self._connection.connect()
        return self._connection.connected()

    def disconnect(self):
        self._connection.disconnect()

    def connected(self):
        return self._connection.connected()

    def authentication_errors_on_machine(self) -> bool:
        return not self._connection.has_available_ports()

    def get_all_values(self) -> DeviceValues:
        response = self._send_to_device(Constants.WRITE_ALL_COMMAND, expect_response=True, data='')
        if response.command != Constants.WRITE_ALL_RESPOND:
            self._logger.log_error(
                "Did not receive expected response with Write all command :" + Constants.WRITE_ALL_RESPOND)
            return None
        return UsbDataMapping.from_data_to_device_values(response.data)

    def set_target_voltage(self, voltage):
        if voltage > 20000:
            return
        self._send_to_device(Constants.SET_VOLTAGE_COMMAND, expect_response=False, data=voltage)

    def set_target_current(self, current):
        if current > 1000:
            return
        self._send_to_device(Constants.SET_CURRENT_COMMAND, expect_response=False, data=current)

    def set_device_is_on(self, is_on):
        command = Constants.SET_OUTPUT_ON_COMMAND
        if is_on:
            one_value = "1"
        else:
            one_value = "0"
        self._send_to_device(command, expect_response=False, data=one_value)

    def _send_to_device(self, command: str, expect_response: bool, data: str) -> DeviceResponse:
        with self._transactionLock:
            serial_data_to_device = UsbDataMapping.to_serial(command, data)
            self._logger.log_sending(serial_data_to_device)
            self._connection.set(serial_data_to_device)
            acknowledgement = self._get_response_from_device()
            self._verify_acknowledgement(acknowledgement)
            if expect_response:
                response = self._get_response_from_device()
                self._verify_crc_code(response)
                return response

    def _get_response_from_device(self) -> DeviceResponse:
        serial_response = self._connection.get()
        device_response = UsbDataMapping.from_serial(serial_response)
        if not device_response:
            return None
        self._logger.log_receiving(device_response.serial_response)
        return device_response

    def _verify_crc_code(self, response: DeviceResponse):
        (error, expected_value, actual_value) = CrcHelper.verify_crc_code(response)
        if error:
            error_message = "Unexpected crc code from device. Got " + actual_value + " but expected " + expected_value
            self._logger.log_error(error_message)

    def _verify_acknowledgement(self, acknowledgement_response: DeviceResponse):
        if not acknowledgement_response:
            raise SerialException("No response from device")
        elif acknowledgement_response.command == Constants.NOT_ACKNOWLEDGE_COMMAND:
            log_string = "Received 'NOT ACKNOWLEDGE' from device."
            self._logger.log_error(log_string)
        elif acknowledgement_response.command != Constants.ACKNOWLEDGE_COMMAND:
            log_string = ("Received neither 'ACKNOWLEDGE' nor 'NOT ACKNOWLEDGE' from device. "
                          "Received : " + acknowledgement_response.decoded_response + " from device")
            self._logger.log_error(log_string)
        self._verify_crc_code(acknowledgement_response)
