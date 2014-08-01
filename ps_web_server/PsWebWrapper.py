import json

from ps_controller.protocol.ProtocolFactory import ProtocolFactory
from ps_controller.DeviceValues import DeviceValues


# TODO document
class Wrapper:
    def __init__(self):
        self._logHandlersAdded = False
        self._hardware_interface = ProtocolFactory().get_protocol("usb")

    def set_voltage(self, voltage: float):
        """
        Set the voltage value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_target_voltage(voltage*1000)

    def set_current(self, current: int):
        """
        Set the current value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_target_current(current)

    def get_current_json(self) -> str:
        """
        Get a JSON object that represents the current device state
        """
        if not self._hardware_interface.connect():
            return ""
        all_values = self._hardware_interface.get_all_values()

        current_values_dict = dict()
        current_values_dict["outputVoltage_V"] = round(all_values.output_voltage / 1000, 1)
        current_values_dict["outputCurrent_mA"] = all_values.output_current
        current_values_dict["inputVoltage_V"] = all_values.input_voltage
        current_values_dict["targetVoltage_V"] = round(all_values.target_voltage / 1000, 1)
        current_values_dict["targetCurrent_mA"] = all_values.target_current
        current_values_dict["outputOn"] = all_values.output_is_on
        current_values_dict["connected"] = self._hardware_interface.connected()

        return json.dumps(current_values_dict)

    def set_device_on(self):
        """
        Turns the currently connected PS201 on. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_device_is_on(True)

    def set_device_off(self):
        """
        Turns the currently connected PS201 off. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_device_is_on(False)

    def connect(self):
        if self._hardware_interface.connected():
            return True
        self._hardware_interface.connect()
        return self._hardware_interface.connected()

    def connected(self):
        return self._hardware_interface.connected()


class MockWrapper(Wrapper):
    def __init__(self):
        self._voltage = 0
        self._current = 0
        super().__init__()

    def get_current_json(self) -> str:
        mock_values = DeviceValues()
        mock_values.output_is_on = False
        mock_values.target_voltage = self._voltage
        mock_values.target_current = self._current
        self._voltage += 0.1
        self._current += 1

        current_values_dict = dict()
        current_values_dict["outputVoltage"] = mock_values.output_voltage
        current_values_dict["outputCurrent"] = mock_values.output_current
        current_values_dict["inputVoltage"] = mock_values.input_voltage
        current_values_dict["preRegVoltage"] = mock_values.pre_reg_voltage
        current_values_dict["targetVoltage"] = mock_values.target_voltage
        current_values_dict["targetCurrent"] = mock_values.target_current
        current_values_dict["outputOn"] = mock_values.output_is_on

        return json.dumps(current_values_dict)

    def set_device_on(self):
        pass

    def set_device_off(self):
        pass

    def set_current(self, current: float):
        self._current = current

    def set_voltage(self, voltage: int):
        self._voltage = voltage

    def connect(self):
        return True

    def connected(self):
        return True