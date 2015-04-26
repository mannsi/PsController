from ps_controller.Constants import Constants
from ps_controller.utilities.Crc import CrcHelper
from ps_controller.DeviceValues import DeviceValues
from ps_controller.DeviceResponse import DeviceResponse


def to_serial(command, data=''):
    """Creates serial code from input parameters

    :param command: PS201 device command
    :type command: str
    :param data: Actual data to/from device
    :type data: str
    :return: bytes -- Serial bytes from input params

    """
    hex_data_length = format(len(str(data)), '02X')

    ascii_string = Constants.START
    ascii_string += command
    ascii_string += hex_data_length
    ascii_string += str(data)
    ascii_string += CrcHelper.create(command, hex_data_length, str(data))
    ascii_string += Constants.END

    return ascii_string.encode('ascii')


def from_serial(serial_value):
    """Decodes serial to an actual device response

    :param serial_value: Serial bytes to decode
    :type serial_value: bytes
    :return: DeviceResponse or None -- A device response if decoding was successful
    """
    response = DeviceResponse()
    try:
        decoded_serial_value = serial_value.decode('ascii')
    except (UnicodeDecodeError, AttributeError):
        return None
    if decoded_serial_value[0:1] != Constants.START:
        return None

    response.command = decoded_serial_value[1:4]
    data_length = int(decoded_serial_value[4:6], 16)
    response.data_length = data_length
    response.data_length_hex = decoded_serial_value[4:6]
    response.data = decoded_serial_value[6: 6 + data_length]
    response.crc = decoded_serial_value[6 + data_length: 10 + data_length]
    response.decoded_response = decoded_serial_value[0:]
    response.serial_response = serial_value[0:]
    if decoded_serial_value[10 + data_length: 11 + data_length] != Constants.END:
        return None

    return response


def from_all_data_to_device_values(data):
    """Converts an 'all data' data string to device values object

    :param data: 'All data' data string
    :type data: str
    :return: DeviceValues or None -- Returns device values if successful
    """
    try:
        split_values = [float(x) for x in data.split(";")]
    except ValueError:
        return None
    if len(split_values) < 5:
        return None
    device_values = DeviceValues()
    device_values.output_voltage = split_values[0]
    device_values.output_current = split_values[1]
    device_values.target_voltage = split_values[2]
    device_values.target_current = split_values[3]
    device_values.output_is_on = bool(split_values[4])
    return device_values