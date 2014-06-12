__author__ = 'mannsi'

import unittest
from ps_controller.utilities.Crc import Crc16
from ps_controller.DeviceResponse import DeviceResponse
from ps_controller.Commands import WriteAllValuesCommand


class TestCrc(unittest.TestCase):
    def setUp(self):
        pass

    def test_bullshit_data_should_not_match(self):
        dummy_device_response = DeviceResponse()
        dummy_device_response.command = WriteAllValuesCommand()
        dummy_device_response.raw_data = bytearray(b'bullshit data')
        self.assertNotEqual(None, Crc16.verify_crc_code(dummy_device_response),
                            'Should not return None because that means crc codes match')

    def test_get_expected_crc_code(self):
        command = WriteAllValuesCommand()
        binary_data = bytearray(b'random data')
        generated_crc_code = Crc16.create(command, binary_data)

        dummy_device_response = DeviceResponse()
        dummy_device_response.command = command
        dummy_device_response.raw_data = binary_data
        dummy_device_response.crc = generated_crc_code
        self.assertEqual(None, Crc16.verify_crc_code(dummy_device_response),
                         'Should return None because the crc code of object should match')