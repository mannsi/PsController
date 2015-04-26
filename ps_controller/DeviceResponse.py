__author__ = 'mannsi'


class DeviceResponse:
    def __init__(self):
        self.command = ""
        self.data_length = 0
        self.data_length_hex = ""
        self.data = ""
        self.crc = ""  # ascii hex string
        self.decoded_response = ""
        self.serial_response = bytes()