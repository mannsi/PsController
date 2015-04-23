from ps_controller import SerialException
from ps_controller.Constants import Constants

__author__ = 'mannsi'

import unittest
from ps_controller.data_mapping.UsbDataMapping import UsbDataMapping


class TestUsbMapping(unittest.TestCase):
    def test_illegal_data_should_return_none(self):
        random_data = "adsf1234"
        incomplete_data = "1;2;3"
        self.assertEqual(None,
                         UsbDataMapping.from_data_to_device_values(random_data),
                         'Random mapping data should return none')
        self.assertEqual(None,
                         UsbDataMapping.from_data_to_device_values(incomplete_data),
                         'Incomplete mapping data should return none')

    def test_converting_to_and_from_should_not_change_data(self):
        command = Constants.WRITE_ALL_COMMAND
        data = "asdf1234"
        serial_value = UsbDataMapping.to_serial(command, data)
        device_value_from_serial = UsbDataMapping.from_serial(serial_value)
        self.assertEquals(command, device_value_from_serial.command,
                          'Command before and after serialization should be equal')
        self.assertEquals(data, device_value_from_serial.data,
                          'Data before and after serialization should be equal')
