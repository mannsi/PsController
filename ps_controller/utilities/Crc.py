import crcmod.predefined

from ..DeviceResponse import DeviceResponse


class CrcHelper:
    @classmethod
    def verify_crc_code(cls, response):
        """Verifies that the crc code in the response is the same as we expect given the response data.

        :param response: The response to verify crc from
        :type response: DeviceResponse
        :return: tuple(bool, str, str) -- Returns (Error, Crc, Expected_Crc)
        """

        """
        Verifies that the crc code in the response is the same as we expect given the response data.
        Returns: (error: bool, expected_crc_code: str, actual_crc_code: str).
        """
        expected_crc_code = CrcHelper.create(response.command, response.data_length_hex, response.data)
        if response.crc != expected_crc_code:
            return True, response.crc, expected_crc_code
        return False, "", ""

    @classmethod
    def create(cls, command, hex_data_length, data):
        """Creates a 4 char hex string from the input parameters

        :param command:
        :type command: str
        :param hex_data_length:
        :type hex_data_length: str
        :param data:
        :type data: str
        :return: str -- 4 char hex string
        """
        joined_string = command + hex_data_length + data
        joined_string_in_bytes = joined_string.encode('ascii')

        crc16 = crcmod.predefined.Crc('xmodem')
        crc16.update(joined_string_in_bytes)
        crc_int_value = crc16.crcValue
        crc_in_hex = format(crc_int_value, '04X')
        return crc_in_hex