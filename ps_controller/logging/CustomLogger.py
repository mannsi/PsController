import os

__author__ = 'mannsi'

import logging
import os

from .CustomLoggerInterface import CustomLoggerInterface


class CustomLogger(CustomLoggerInterface):
    def __init__(self, log_level):
        logger_name = "PS201Logger"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(os.path.join(os.path.expanduser('~'), 'PS201.log'))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        print_handler = logging.StreamHandler()
        print_handler.setFormatter(formatter)
        self.logger.addHandler(print_handler)
        self.logger.setLevel(log_level)

    def log_error(self, error_message):
        self.logger.log(logging.ERROR, error_message)

    def log_debug(self, message):
        self.logger.log(logging.INFO, message)

    def log_sending(self, message: bytes):
        log_string = "Sending data: " + message.decode("ascii")
        self.logger.log(logging.DEBUG, log_string)

    def log_receiving(self, message: bytes):
        log_string = "Received data:" + message.decode("ascii")
        self.logger.log(logging.DEBUG, log_string)