import json
from ps_controller import SerialException

from ps_controller.protocol.ProtocolFactory import ProtocolFactory
from ps_controller.DeviceValues import DeviceValues


class Wrapper:
    def __init__(self):
        self._logHandlersAdded = False
        self._hardware_interface = ProtocolFactory().get_protocol("usb")

    def set_voltage(self, voltage: int):
        """
        Set the voltage value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_target_voltage(int(voltage*1000))

    def set_current(self, current: int):
        """
        Set the current value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_target_current(current)

    def get_all_values_json(self) -> str:
        """
        Get a JSON object that represents the current device state
        """
        all_values = DeviceValues()
        current_values_dict = dict()
        try:
            if self._hardware_interface.connect():
                all_values = self._hardware_interface.get_all_values()

            current_values_dict["output_voltage_V"] = round(all_values.output_voltage / 1000, 1)
            current_values_dict["output_current_mA"] = all_values.output_current
            current_values_dict["target_voltage_V"] = round(all_values.target_voltage / 1000, 1)
            current_values_dict["current_limit_mA"] = all_values.target_current
            current_values_dict["output_on"] = 1 if all_values.output_is_on else 0
            current_values_dict["connected"] = 1 if self._hardware_interface.connect() else 0
        except Exception:
            current_values_dict["output_voltage_V"] = 0
            current_values_dict["output_current_mA"] = 0
            current_values_dict["target_voltage_V"] = 0
            current_values_dict["current_limit_mA"] = 0
            current_values_dict["output_on"] = 0
            current_values_dict["connected"] = 0

        return json.dumps(current_values_dict)

    def get_current_mA(self) -> str:
        """
        Returns the actual current of the device as string.
        """
        if not self._hardware_interface.connect():
            return ""
        all_values = self._hardware_interface.get_all_values()
        return str(all_values.output_current)

    def get_voltage_V(self) -> str:
        """
        Returns the actual voltage of the device as string
        """
        if not self._hardware_interface.connect():
            return ""
        all_values = self._hardware_interface.get_all_values()
        return str(round(all_values.output_voltage / 1000, 1))

    def get_output_on(self) -> bool:
        """
        Returns bool if output is on or not
        """
        if not self._hardware_interface.connect():
            return ""
        all_values = self._hardware_interface.get_all_values()
        return all_values.output_is_on

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
        if not self._hardware_interface.connected():
            return
        self._hardware_interface.set_device_is_on(False)

    def connect(self):
        if self._hardware_interface.connected():
            return True
        self._hardware_interface.connect()
        return self._hardware_interface.connected()

    def connected_json(self):
        connected = self._hardware_interface.connect()
        return_value = dict()
        return_value["connected"] = 1 if connected else 0
        return_value["authentication_error"] = 0 if connected else (1 if self._authentication_errors() else 0)
        return json.dumps(return_value)

    def _authentication_errors(self):
        return self._hardware_interface.authentication_errors_on_machine()


class MockWrapper(Wrapper):
    def __init__(self):
        self._voltage = 0
        self._current = 0
        super().__init__()

    def get_all_values_json(self) -> str:
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

    def _connected(self):
        return True