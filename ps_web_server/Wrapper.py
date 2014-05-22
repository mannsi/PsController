import json
import time

from ps_controller.HardwareInterface import HardwareInterface
from ps_controller.protocol.ProtocolFactory import ProtocolFactory


class Wrapper:
    def __init__(self):
        protocol = ProtocolFactory().get_protocol("usb")
        self._hardware_interface = HardwareInterface(protocol)
        self.json_data_since_star = ''

    def set(self, voltage, current):
        """
        Set the values of the connected PS201.
        Voltage is a float in unit V and current is an int in unit mA
        """
        if not self._hardware_interface.connected():
            raise Exception("Not connected")
        self._hardware_interface.set_target_voltage(voltage)
        self._hardware_interface.set_target_current(current)

    def get(self):
        """
        Gets a JSON object that represents the current device state
        """
        if not self._hardware_interface.connected():
            raise Exception("Not connected")
        all_values = self._hardware_interface.get_all_values()
        self.add_all_values_to_json(all_values)
        return self.json_data_since_star

    def connect(self):
        if self._hardware_interface.connected():
            return True
        self._hardware_interface.connect()
        return self._hardware_interface.connected()

    def connected(self):
        return self._hardware_interface.connected

    def add_all_values_to_json(self, all_values):
        self.json_data_since_star += json.dumps({time.time(): all_values.to_JSON()})

wrapper = Wrapper()
connected = wrapper.connect()