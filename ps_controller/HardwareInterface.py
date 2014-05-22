

class HardwareInterface:
    def __init__(self, protocol):
        self._protocol = protocol

    def connect(self):
        return self._protocol.connect()

    def connected(self):
        return self._protocol.connected()

    def set_target_voltage(self, voltage):
        self._protocol.set_target_voltage(voltage)

    def set_target_current(self, current):
        self._protocol.set_target_current(current)

    def set_device_is_on(self, is_on):
        self._protocol.set_device_is_on(is_on)

    def get_all_values(self):
        values = self._protocol.get_all_values()
        return values