from ..Constants import Constants
from ..utilities.Crc import Crc16
from ..DeviceValues import DeviceValues
from ..DeviceResponse import DeviceResponse
from ps_controller import SerialException
import ps_controller.Commands as Commands


class UsbDataMapping():
    @classmethod
    def to_serial(cls, command: Commands.BaseCommand, data='') -> bytearray:
        """
        Returns a bytearray containing serial code made from 'command' and 'data'
        """
        binary_data = bytes(str(data), 'ascii')
        crc_code = Crc16.create(command, binary_data)
        data_length = len(binary_data)

        byte_array = bytearray()
        byte_array.append(Constants.START)
        byte_array.append(command.int_value())
        byte_array.append(data_length)
        if data_length > 0:
            for intData in binary_data:
                byte_array.append(intData)
        for crc in crc_code:
            byte_array.append(crc)
        byte_array.append(Constants.START)
        return byte_array

    @classmethod
    def from_serial(cls, serial_value: bytearray) -> DeviceResponse:
        """Converts a bytes object into a device response object"""
        response = DeviceResponse()
        try:
            response.start = serial_value[0]
            response.command = Commands.get_command(serial_value[1])
            response.data_length = serial_value[2]
            index = 3
            response.raw_data = serial_value[index:index + response.data_length]
            response.data = response.raw_data.decode()
            index += response.data_length
            response.crc = []
            while True:
                value = serial_value[index]
                if value == Constants.START:
                    break
                response.crc.append(value)
                index += 1
                if index >= len(serial_value):
                    raise Exception("End char missing. Received %s" % serial_value)
            response.end = serial_value[index]
            response.serial_response = serial_value
            cls._set_readable_serial_value(response)
        except Exception as e:
            raise SerialException("Error mapping values from serial. Message " + e.args[0])
        return response

    @staticmethod
    def from_data_to_device_values(data: str) -> DeviceValues:
        """
        Takes data from PS201 and converts it into DeviceValues object

        Parameters
        ----------
        data: Comma separated string of values
        """
        try:
            split_values = [float(x) for x in data.split(";")]
        except ValueError as e:
            return None
        if len(split_values) < 7:
            return None
        device_values = DeviceValues()
        device_values.output_voltage = split_values[0]
        device_values.output_current = split_values[1]
        device_values.target_voltage = split_values[2]
        device_values.target_current = split_values[3]
        device_values.pre_reg_voltage = split_values[4]
        device_values.input_voltage = split_values[5]
        device_values.output_is_on = bool(split_values[6])
        return device_values

    @classmethod
    def _set_readable_serial_value(cls, response: DeviceResponse):
        """
        Sets the response.readable_serial to nicer values.
        """
        response.readable_serial.append(cls._printable_hex(response.start))
        response.readable_serial.append(cls._printable_hex(response.command.int_value()))
        response.readable_serial.append(cls._printable_hex(response.data_length))
        if response.raw_data:
            response.readable_serial.append(response.raw_data.decode("utf-8"))
        for crc in response.crc:
            response.readable_serial.append(cls._printable_hex(crc))
        response.readable_serial.append(cls._printable_hex(response.start))

    @staticmethod
    def _printable_hex(int_value: int) -> str:
        hex_string = format(int_value, 'x')
        if len(hex_string) == 1:
            hex_string = '0' + hex_string
        return hex_string