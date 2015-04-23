__author__ = 'mannsi'


class CustomLoggerInterface:
    def log_sending(self, message: bytes):
        raise NotImplementedError()

    def log_receiving(self, message: bytes):
        raise NotImplementedError()

    def log_error(self, error_message: str):
        raise NotImplementedError()

    def log(self, message: str):
        raise NotImplementedError()