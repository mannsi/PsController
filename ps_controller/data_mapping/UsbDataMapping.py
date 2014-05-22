from ..Constants import *
from ..utilities.Crc import Crc16


class UsbDataMapping():
    @classmethod
    def to_serial(cls, command, data=''):
        binary_data = bytes(str(data), 'ascii')
        crc_code = Crc16.create(command, binary_data)
        data_length = len(binary_data)

        byte_array = bytearray()
        byte_array.append(START)
        byte_array.append(command)
        byte_array.append(data_length)
        if data_length > 0:
            for intData in binary_data:
                byte_array.append(intData)
        for crc in crc_code:
            byte_array.append(crc)
        byte_array.append(START)
        return byte_array

    @classmethod
    def from_serial(cls, serial_value):
        """Converts a bytes object into a device response object"""
        response = _DeviceResponse()
        try:
            response.start = serial_value[0]
            response.command = serial_value[1]
            response.data_length = serial_value[2]
            index = 3
            response.raw_data = serial_value[index:index + response.data_length]
            response.data = response.raw_data.decode()
            index += response.data_length
            response.crc = []
            while True:
                value = serial_value[index]
                if value == START:
                    break
                response.crc.append(value)
                index += 1
                if index >= len(serial_value):
                    raise Exception("End char missing. Received %s" % serial_value)
            response.end = serial_value[index]
            response.serial_response = serial_value
            cls._set_readable_serial_value(response)
        except Exception as e:
            raise SerialException(e.args[0])
        return response

    @classmethod
    def _set_readable_serial_value(cls, response):
        response.readableSerial.append(cls._printable_hex(response.start))
        response.readableSerial.append(cls._printable_hex(response.command))
        response.readableSerial.append(cls._printable_hex(response.dataLength))
        if response.rawData:
            response.readableSerial.append(response.rawData.decode("utf-8"))
        for crc in response.crc:
            response.readableSerial.append(cls._printable_hex(crc))
        response.readableSerial.append(cls._printable_hex(response.end))

    @staticmethod
    def _printable_hex(int_value):
        hex_string = format(int_value, 'x')
        if len(hex_string) == 1:
            hex_string = '0' + hex_string
        return hex_string


class _DeviceResponse:
    def __init__(self):
        self.start = 0
        self.command = 0
        self.data_length = 0
        self.data = ""
        self.crc = []  # list of int values
        self.serial_response = bytearray()
        self.readable_serial = []


class SerialException(Exception):
    pass