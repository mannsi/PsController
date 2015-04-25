__author__ = 'mannsi'

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
            raise Exception("Trying to read when connection is closed")
        return_value = self._return_read_value[0:number_of_bytes]
        self._return_read_value = self._return_read_value[number_of_bytes:]
        return return_value

    def write(self, data):
        if not self._connected:
            raise Exception("Trying to write when connection is closed")
        pass

    def set_read_return_value(self, data):
        self._return_read_value = data


class MockLogger(CustomLoggerInterface):
    def log_sending(self, message: bytes):
        pass

    def log_receiving(self, message: bytes):
        pass

    def log_error(self, error_message: str):
        pass

    def log(self, message: str):
        pass