import threading

from .BaseProtocolInterface import BaseProtocolInterface
from ..data_mapping.UsbDataMapping import UsbDataMapping
from ps_controller import SerialException
from ..utilities.Crc import Crc16
from ..DeviceResponse import DeviceResponse
from ..Commands import *
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
        self.logger = logger
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
        response = self._send_to_device(WriteAllValuesCommand(), expect_response=True, data='')
        return UsbDataMapping.from_data_to_device_values(response.data)

    def set_target_voltage(self, voltage):
        if voltage > 20000:
            return
        self._send_to_device(ReadTargetVoltageCommand(), expect_response=False, data=voltage)

    def set_target_current(self, current):
        if current > 1000:
            return
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
            self.logger.log_sending(command, data, serial_data_to_device)
            self._connection.set(serial_data_to_device)
            acknowledgement = self._get_response_from_device()
            self._verify_acknowledgement(acknowledgement, command)
            if expect_response:
                response = self._get_response_from_device()
                self._verify_crc_code(response)
                return response

    def _get_response_from_device(self) -> DeviceResponse:
        serial_response = self._connection.get()
        if not serial_response:
            return None
        device_response = UsbDataMapping.from_serial(serial_response)
        self.logger.log_receiving(device_response)
        return device_response

    def _verify_crc_code(self, response: DeviceResponse):
        crc_return_value = Crc16.verify_crc_code(response)
        if crc_return_value:
            error_message = ("Unexpected crc code from device. Got " +
                             ','.join(str(x) for x in crc_return_value[0]) +
                             " but expected " +
                             ','.join(str(x) for x in crc_return_value[1]))
            self.logger.log_error(error_message)

    def _verify_acknowledgement(self, acknowledgement_response: DeviceResponse, command: BaseCommand):
        if not acknowledgement_response:
            raise SerialException("No response from device when sending '" + command.readable() + "'")
        elif acknowledgement_response.command == NotAcknowledgementCommand():
            log_string = ("Received 'NOT ACKNOWLEDGE' from device."
                          "Command sent to device: '" + command.readable() + "'")
            self.logger.log_error(log_string)
        elif acknowledgement_response.command != AcknowledgementCommand():
            log_string = ("Received neither 'ACKNOWLEDGE' nor 'NOT ACKNOWLEDGE' from device. "
                          "Command sent to device: '" + command.readable() + "'."
                          "Received command: " + acknowledgement_response.command.readable() + " from device")
            self.logger.log_error(log_string)
        self._verify_crc_code(acknowledgement_response)
