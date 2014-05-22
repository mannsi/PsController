

class BaseProtocolInterface:
    def __init__(self, connection):
        self._connection = connection

    def connect(self):
        raise NotImplementedError()

    def connected(self):
        raise NotImplementedError()

    def get_all_values(self):
        raise NotImplementedError()

    def set_target_voltage(self, voltage):
        raise NotImplementedError()

    def set_target_current(self, current):
        raise NotImplementedError()

    def set_device_is_on(self, is_on):
        raise NotImplementedError()

