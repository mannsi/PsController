import logging
import threading

from apscheduler.scheduler import Scheduler

from .BaseProtocolInterface import BaseProtocolInterface
from ..data_mapping.UsbDataMapping import UsbDataMapping
from ..Constants import Constants
from ..utilities.Crc import Crc16
from ..DeviceResponse import DeviceResponse
from ..Commands import *
from ..DeviceValues import DeviceValues


class UsbProtocol(BaseProtocolInterface):
    def __init__(self, connection):
        """
        Parameters
        ----------
        Connection : BaseConnectionInterface object
        """
        super(UsbProtocol, self).__init__(connection)
        self.streaming_scheduler = Scheduler()
        self._transactionLock = threading.Lock()
        self._current_stream_values = DeviceValues()
        self._stream_lock = threading.Lock()

    def connect(self):
        self._connection.connect()
        return self._connection.connected()

    def disconnect(self):
        self._connection.disconnect()

    def connected(self):
        return self._connection.connected()

    def get_all_values(self):
        return self._current_stream_values
        # response = self._send_to_device(WriteAllValuesCommand(), expect_response=True, data='')
        # return UsbDataMapping.from_data_to_device_values(response.data)

    def set_target_voltage(self, voltage):
        with self._stream_lock:
            self._current_stream_values.target_voltage = voltage
        self._send_to_device(ReadTargetVoltageCommand(), expect_response=False, data=voltage)

    def set_target_current(self, current):
        with self._stream_lock:
            self._current_stream_values.target_current = current
        self._send_to_device(ReadTargetCurrentCommand(), expect_response=False, data=current)

    def set_device_is_on(self, is_on):
        with self._stream_lock:
            self._current_stream_values.output_is_on = is_on
            if is_on:
                command = TurnOnOutputCommand()
            else:
                command = TurnOffOutputCommand()
        self._send_to_device(command, expect_response=False, data='')

    def start_streaming(self):
        # Send start streaming command to device
        self._send_to_device(StartStreamCommand(), False, '')

        # Initialize streaming values. Streaming update only updates this value
        with self._stream_lock:
            self._current_stream_values = self.get_all_values()

        # Start a timer that reads from the streaming_values_buffer
        self.streaming_scheduler.start()
        self.streaming_scheduler.add_interval_job(self._get_stream_values, seconds=0.5, args=[])

    def get_current_streaming_values(self) -> DeviceValues:
        with self._stream_lock:
            return self._current_stream_values

    def _get_stream_values(self):
        try:
            response_list = []
            with self._transactionLock:
                response = self._get_response_from_device()
                while response:
                    response_list.append(response)
                    response = self._get_response_from_device()
            if not response_list:
                return
            [self._verify_crc_code(response, StartStreamCommand(), '') for response in response_list]

            with self._stream_lock:
                for response in response_list:
                    command = response.command
                    value = response.data
                    if command == WriteOutputVoltageCommand():
                        self._current_stream_values.output_voltage = float(value)
                    elif command == WriteOutputCurrentCommand():
                        self._current_stream_values.output_current = int(value)
                    elif command == WritePreRegVoltageCommand():
                        self._current_stream_values.pre_reg_voltage = float(value)
                    elif command == WriteTargetVoltageCommand():
                        self._current_stream_values.target_voltage = float(value)
                    elif command == WriteTargetCurrentCommand():
                        self._current_stream_values.target_current = int(value)
                    elif command == WriteIsOutputOnCommand():
                        self._current_stream_values.output_is_on = bool(value)
                    elif command == WriteInputVoltageCommand():
                        self._current_stream_values.input_voltage = float(value)
        except Exception as e:
            logging.getLogger(Constants.LOGGER_NAME).exception(e)

    def _send_to_device(self, command: BaseCommand, expect_response: bool, data) -> DeviceResponse:
        with self._transactionLock:
             # Clear buffer in case there are some streaming values still there
            self._connection.clear_buffer()
            serial_data_to_device = UsbDataMapping.to_serial(command, data)
            self._connection.set(serial_data_to_device)
            acknowledgement = self._get_response_from_device()
            UsbProtocol._verify_acknowledgement(acknowledgement, command, data='')
            if expect_response:
                response = self._get_response_from_device()
                UsbProtocol._verify_crc_code(response, command, data='')
                return response

    def _get_response_from_device(self) -> DeviceResponse:
        serial_response = self._connection.get()
        if not serial_response:
            return None
        return UsbDataMapping.from_serial(serial_response)

    @classmethod
    def _verify_crc_code(cls, response: DeviceResponse, command: BaseCommand, data):
        crc_return_value = Crc16._verify_crc_code(response)
        if crc_return_value:
            error_message = ("Unexpected crc code from device. Got " +
                             crc_return_value[0] + " but expected " + crc_return_value[1])
            cls._log_transmission_error(error_message, command, data, response)

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
        cls._verify_crc_code(acknowledgement_response, command, data)

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