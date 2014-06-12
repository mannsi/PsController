import crcmod.predefined

from ..Constants import Constants
from ..DeviceResponse import DeviceResponse
from ..Commands import BaseCommand

# Int values of characters to escape
_characters_to_escape = [Constants.START, Constants.ESCAPE, Constants.NEW_LINE, Constants.RETURN]


class Crc16:
    @classmethod
    def verify_crc_code(cls, response: DeviceResponse):
        """
        Verifies that the crc code in the response is the same as we expect given the response data.
        Returns: None if crc codes match, otherwise tuple containing (received_crc_code, expected_crc_code).
        """
        expected_crc_code = Crc16.create(response.command, response.raw_data)
        if response.crc != expected_crc_code:
            return response.crc, expected_crc_code
        return None

    @classmethod
    def create(cls, command: BaseCommand, binary_data: bytes):
        """
        Returns a list of ints containing the crc code from input values
        """
        bytes_command = bytes([command.int_value()])
        crc16 = crcmod.predefined.Crc('xmodem')
        crc16.update(bytes_command)
        crc16.update(bytes([len(binary_data)]))
        crc16.update(binary_data)
        unescaped_hex_crc = cls._get_hex_list_from_int(crc16.crcValue)
        escaped_int_crc = cls._escape_crc_code(unescaped_hex_crc, _characters_to_escape)
        return escaped_int_crc

    @staticmethod
    def _escape_crc_code(unescaped_crc_code: list, values_to_escape: list):
        """
        Escapes a list of hex crc values and returns an int crc list

        Parameters
        ----------
        unescaped_crc_code: [hex]
        values_to_escape: [int]
        """
        crc_code = []
        for unescapedCrcByte in unescaped_crc_code:
            int_crc_value = int(unescapedCrcByte, 16)
            if int_crc_value in values_to_escape:
                crc_code.append(Constants.ESCAPE)
                crc_code.append(Constants.FLIP ^ int_crc_value)
            else:
                crc_code.append(int_crc_value)
        return crc_code

    @staticmethod
    def _get_hex_list_from_int(int_value: int) -> list:
        """Splits a 4 char hex code into 2x 2 char hex code i.e 0x1234 becomes [0x12, 0x34]"""
        return [hex(x) for x in divmod(int_value, 0x100)]
