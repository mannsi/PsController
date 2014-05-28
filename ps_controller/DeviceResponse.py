__author__ = 'mannsi'
from .Commands import BaseCommand


class DeviceResponse:
    def __init__(self):
        self.start = 0
        self.command = BaseCommand()
        self.data_length = 0
        self.data = ""
        self.crc = []  # list of int values
        self.serial_response = bytearray()
        self.readable_serial = []
        self.raw_data = bytearray()