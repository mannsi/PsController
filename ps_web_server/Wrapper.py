import json
import time
import logging

from ps_controller.protocol.ProtocolFactory import ProtocolFactory
from ps_controller.Constants import Constants
from ps_controller.DeviceValues import DeviceValues


class Wrapper:
    def __init__(self):
        self._hardware_interface = ProtocolFactory().get_protocol("usb")
        self._logHandlersAdded = False
        self._set_logging(logging.DEBUG)
        self._all_values_dict = dict()
        self._all_values_dict["voltage"] = dict()
        self._all_values_dict["voltage"]["datasets"] = [{"data": []}]
        self._all_values_dict["voltage"]["datasets"][0]["strokeColor"] = "rgba(0,0,0,1)"
        self._all_values_dict["voltage"]["labels"] = []
        self._all_values_dict["current"] = dict()
        self._all_values_dict["current"]["datasets"] = [{"data": []}]
        self._all_values_dict["current"]["datasets"][0]["strokeColor"] = "rgba(0,0,0,1)"
        self._all_values_dict["current"]["labels"] = []

    def set_voltage(self, voltage: float):
        """
        Set the voltage value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        self._hardware_interface.set_target_voltage(voltage)

    def set_current(self, current: int):
        """
        Set the current value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        self._hardware_interface.set_target_current(current)

    def get_values(self) -> DeviceValues:
        """
        Returns the current device values of the PS201. Raises a serial.Serial exception if not connected
        """
        return self._hardware_interface.get_all_values()

    def get_current_json(self) -> str:
        """
        Get a JSON object that represents the current device state
        """
        all_values = self.get_values()

        current_values_dict = dict()
        current_values_dict["outputVoltage"] = all_values.output_voltage
        current_values_dict["outputCurrent"] = all_values.output_current
        current_values_dict["inputVoltage"] = all_values.input_voltage
        current_values_dict["preRegVoltage"] = all_values.pre_reg_voltage
        current_values_dict["targetVoltage"] = all_values.target_voltage
        current_values_dict["targetCurrent"] = all_values.target_current
        current_values_dict["outputOn"] = all_values.output_is_on

        return json.dumps(current_values_dict)

    def get_all_json(self) -> str:
        """
        Gets a JSON object that represents all device states since start
        """
        if not self.connected():
            raise Exception("Not connected")
        all_values = self.get_values()
        if all_values:
            self._add_all_values_to_json(all_values)
        return json.dumps(self._all_values_dict)

    def set_device_on(self):
        """
        Turns the currently connected PS201 on. Raises a serial.Serial exception if not connected
        """
        self._hardware_interface.set_device_is_on(True)

    def set_device_off(self):
        """
        Turns the currently connected PS201 off. Raises a serial.Serial exception if not connected
        """
        self._hardware_interface.set_device_is_on(False)

    def connect(self):
        if self._hardware_interface.connected():
            return True
        self._hardware_interface.connect()
        return self._hardware_interface.connected()

    def connected(self):
        return self._hardware_interface.connected

    def _add_all_values_to_json(self, all_values: DeviceValues):
        self._all_values_dict["voltage"]["datasets"][0]["data"].append(all_values.target_voltage)
        self._all_values_dict["voltage"]["labels"].append("")
        self._all_values_dict["current"]["datasets"][0]["data"].append(all_values.target_current)
        self._all_values_dict["current"]["labels"].append("")

    def _set_logging(self, log_level):
        if not self._logHandlersAdded:
            logger = logging.getLogger(Constants.LOGGER_NAME)
            logger.propagate = False
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler = logging.FileHandler("PS201.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            print_handler = logging.StreamHandler()
            print_handler.setFormatter(formatter)
            logger.addHandler(print_handler)
            self._logHandlersAdded = True

            # Overwhelming when this is set to debug
            logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)

        logging.getLogger(Constants.LOGGER_NAME).setLevel(log_level)


class MockWrapper(Wrapper):
    def __init__(self):
        super().__init__()
        self.voltage = 1
        self.current = 0

    def get_values(self) -> DeviceValues:
        mock_values = DeviceValues()
        mock_values.target_voltage = self.voltage
        mock_values.target_current = self.current
        self.voltage += 0.1
        self.current += 1
        return mock_values

    def set_device_on(self):
        pass

    def set_device_off(self):
        pass

    def set_current(self, current: float):
        pass

    def set_voltage(self, voltage: int):
        pass

    def connect(self):
        return True

    def connected(self):
        return True