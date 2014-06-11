import threading

from apscheduler.scheduler import Scheduler

from .BaseProtocolInterface import BaseProtocolInterface
from ..data_mapping.UsbDataMapping import UsbDataMapping
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

    def get_current_stream_values(self):
        return self._current_stream_values

    def get_all_values(self):
        response = self._send_to_device(WriteAllValuesCommand(), expect_response=True, data='')
        return UsbDataMapping.from_data_to_device_values(response.data)

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
        self.streaming_scheduler.add_interval_job(self._get_stream_values, seconds=0.2, args=[])

    def stop_streaming(self):
        self._send_to_device(StopStreamCommand(), False, '')
        self.streaming_scheduler.shutdown(wait=False)
        self._connection.clear_buffer()

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
            [self._verify_crc_code(response) for response in response_list]

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
            self.logger.log_error("Error getting stream values. Message: " + str(e))

    def _send_to_device(self, command: BaseCommand, expect_response: bool, data) -> DeviceResponse:
        with self._transactionLock:
            # Clear buffer in case there are some streaming values still there
            self._connection.clear_buffer()
            serial_data_to_device = UsbDataMapping.to_serial(command, data)
            self.logger.log_sending(command, data, self.readable_serial_from_serial(serial_data_to_device))
            self._connection.set(serial_data_to_device)
            acknowledgement = self._get_response_from_device()
            self._verify_acknowledgement(acknowledgement, command, data='')
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

    def readable_serial_from_serial(self, serial):
        return ''.join(UsbDataMapping.from_serial(serial).readable_serial)

    def _verify_crc_code(self, response: DeviceResponse):
        crc_return_value = Crc16._verify_crc_code(response)
        if crc_return_value:
            error_message = ("Unexpected crc code from device. Got " +
                             crc_return_value[0] + " but expected " + crc_return_value[1])
            self.logger.log_error(error_message)

    def _verify_acknowledgement(self, acknowledgement_response: DeviceResponse, command: BaseCommand, data):
        if not acknowledgement_response:
            self.logger.log_error("No response from device when sending '" + command.readable() + "'")
        elif acknowledgement_response.command == NotAcknowledgementCommand():
            log_string = ("Received 'NOT ACKNOWLEDGE' from device."
                          "Command sent to device: '" + command.readable() + "'")
            self.logger.log_error(log_string, command, data, acknowledgement_response)
        elif acknowledgement_response.command != AcknowledgementCommand():
            log_string = ("Received neither 'ACKNOWLEDGE' nor 'NOT ACKNOWLEDGE' from device. "
                          "Command sent to device: '" + command.readable() + "'."
                          "Received command: " + acknowledgement_response.command.readable() + " from device")
            self.logger.log_error(log_string)
        self._verify_crc_code(acknowledgement_response)
