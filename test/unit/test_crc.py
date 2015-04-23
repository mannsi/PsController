__author__ = 'mannsi'

import unittest
from ps_controller.utilities.Crc import CrcHelper
from ps_controller.DeviceResponse import DeviceResponse


class TestCrc(unittest.TestCase):
    def setUp(self):
        pass

    def test_bullshit_data_should_not_match(self):
        dummy_device_response = DeviceResponse()
        dummy_device_response.command = "RND"
        dummy_device_response.data_length_hex = "AB"
        dummy_device_response.data = "Random data"
        self.assertEqual(1,
                         CrcHelper.verify_crc_code(dummy_device_response)[0],
                         'Dummy data should not be ')

    def test_get_expected_crc_code(self):
        command = "WRT"
        hex_length = "04"
        data = "1000"
        pre_calculated_crc = "D445"

        generated_crc_code = CrcHelper.create(command, hex_length, data)

        self.assertEqual(pre_calculated_crc, generated_crc_code,
                         'Pre calculated crc and generated crc should match')