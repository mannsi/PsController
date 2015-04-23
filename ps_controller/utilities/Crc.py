import crcmod.predefined

from ..DeviceResponse import DeviceResponse


class CrcHelper:
    @classmethod
    def verify_crc_code(cls, response: DeviceResponse):
        """
        Verifies that the crc code in the response is the same as we expect given the response data.
        Returns: (error: bool, expected_crc_code: str, actual_crc_code: str).
        """
        expected_crc_code = CrcHelper.create(response.command, response.data_length_hex, response.data)
        if response.crc != expected_crc_code:
            return 1, response.crc, expected_crc_code
        return 0, "", ""

    @classmethod
    def create(cls, command: str, hex_data_length: str, data: str) -> str:
        """
        Returns crc value in 4 char hex string
        """
        joined_string = command + hex_data_length + data
        joined_string_in_bytes = joined_string.encode('ascii')

        crc16 = crcmod.predefined.Crc('xmodem')
        crc16.update(joined_string_in_bytes)
        crc_int_value = crc16.crcValue
        crc_in_hex = format(crc_int_value, '04X')
        return crc_in_hex

    @staticmethod
    def _get_hex_list_from_int(int_value: int) -> list:
        """Splits a 4 char hex code into 2x 2 char hex code i.e 0x1234 becomes [0x12, 0x34]"""
        return [hex(x) for x in divmod(int_value, 0x100)]
