__author__ = 'mannsi'

from ps_controller import SerialException
from ps_controller.connection.BaseConnectionInterface import BaseConnectionInterface
from ps_controller.Constants import Constants
from ps_controller.logging.CustomLoggerInterface import CustomLoggerInterface


class MockSerialLink:
    def __init__(self, baud_rate, timeout):
        self._port = None
        self._baud_rate = baud_rate
        self._timeout = timeout

        self._connected = False
        self._return_read_value = []

    def open(self):
        self._connected = True

    def close(self):
        self._connected = False

    def isOpen(self):
        return self._connected

    def flushInput(self):
        self._return_read_value = []

    def read(self, number_of_bytes):
        if not self._connected:
            raise SerialException("Trying to read when connection is closed")
        return_value = self._return_read_value[0:number_of_bytes]
        self._return_read_value = self._return_read_value[number_of_bytes:]
        return return_value

    def write(self, data):
        if not self._connected:
            raise SerialException("Trying to write when connection is closed")
        pass

    def set_read_return_value(self, data):
        self._return_read_value = data


class MockConnection(BaseConnectionInterface):
    def __init__(self):
        self._connected = False
        self._binary_data_in_buffer = []

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def connected(self):
        return self._connected

    def get(self):
        if not self._connected:
            raise SerialException("Trying to set when closed connection")

        if not self._binary_data_in_buffer:
            return bytearray()
        try:
            line = bytearray()
            start_count = 0
            while True:
                c = self._binary_data_in_buffer.pop(0)
                line.append(c)
                if c == Constants.START:
                    start_count += 1
                if start_count == 2:
                    break
            return line
        except Exception as e:
            raise SerialException(e)

    def set(self, sending_data):
        if not self._connected:
            raise SerialException("Trying to set when closed connection")

    def set_binary_buffer_data(self, data):
        self._binary_data_in_buffer = data


class MockLogger(CustomLoggerInterface):
    def log_sending(self, command, data, serial):
        pass

    def log_receiving(self, device_response):
        pass

    def log_error(self, error_message: str):
        pass

    def log_info(self, info_message: str):
        pass