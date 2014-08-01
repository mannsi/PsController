__author__ = 'mannsi'

import logging

from ..DeviceResponse import DeviceResponse
from .CustomLoggerInterface import CustomLoggerInterface
from ..Commands import BaseCommand


class CustomLogger(CustomLoggerInterface):
    def __init__(self):
        log_level = logging.ERROR
        logger_name = "PS201Logger"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler("PS201.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        print_handler = logging.StreamHandler()
        print_handler.setFormatter(formatter)
        self.logger.addHandler(print_handler)
        self.logger.setLevel(log_level)

    def log_error(self, error_message):
        self.logger.log(logging.ERROR, error_message)

    def log_info(self, info_message):
        self.logger.log(logging.INFO, info_message)

    def log_sending(self, command, data, serial: bytearray):
        log_string = "Command " + command.readable() + " sent to device with data " + str(data)
        self.logger.log(logging.DEBUG, log_string)

    def log_receiving(self, device_response):
        log_string = "Data received from device:" + ''.join(device_response.readable_serial)
        self.logger.log(logging.DEBUG, log_string)