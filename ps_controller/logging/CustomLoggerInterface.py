__author__ = 'mannsi'


class CustomLoggerInterface:
    def log_sending(self, message):
        """Log a message that is being sent to device

        :param message: The bytes being sent
        :type message: bytes
        :return: None
        """
        raise NotImplementedError()

    def log_receiving(self, message):
        """Log a message received from device

        :param message: The message received
        :type message: bytes
        :return: None
        """
        raise NotImplementedError()

    def log_error(self, error_message):
        """Log an error message

        :param error_message: The error message
        :type error_message: str
        :return: None
        """
        raise NotImplementedError()

    def log_debug(self, message):
        """Log a debug message

        :param message: The debug message
        :type message: str
        :return: None
        """
        raise NotImplementedError()