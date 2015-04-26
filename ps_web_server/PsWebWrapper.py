import json
from ps_controller import PsControllerException
from ps_controller.DeviceValues import DeviceValues
from ps_controller.logging.CustomLogger import CustomLogger

from ps_controller.device.DeviceFactory import DeviceFactory


class Wrapper:
    """ Abstracts communication to the device for the PsWebServer"""
    def __init__(self, log_level):
        self._logHandlersAdded = False
        logger = CustomLogger(log_level)
        self._hardware_interface = DeviceFactory().get_device("usb", logger)

    def set_voltage(self, voltage):
        """Set the voltage value of the connected PS201

        :param voltage: The voltage to set. Unit is V
        :type voltage: float
        :return: None
        """
        self._hardware_interface.connect()
        try:
            self._hardware_interface.set_target_voltage(int(voltage*1000))
        except PsControllerException:
            pass

    def set_current(self, current):
        """Set the current value of the connected PS201

        :param current: The current to set. Unit is mA
        :type current: int
        :return: None
        """
        self._hardware_interface.connect()
        try:
            self._hardware_interface.set_target_current(current)
        except PsControllerException:
            pass

    def get_all_values_json(self):
        """Get all device values on JSON format

        :return: str -- JSON str dict of device values with the following keys::
            - output_voltage_V
            - output_current_mA
            - target_voltage_V
            - current_limit_mA
            - output_on
            - connected
        """
        current_values_dict = dict()
        self._hardware_interface.connect()
        try:
            all_values = self._hardware_interface.get_all_values()
            current_values_dict["connected"] = 1 if self._hardware_interface.connected() else 0
        except PsControllerException:
            all_values = DeviceValues()
            current_values_dict["connected"] = 0

        current_values_dict["output_voltage_V"] = round(all_values.output_voltage / 1000, 1)
        current_values_dict["output_current_mA"] = all_values.output_current
        current_values_dict["target_voltage_V"] = round(all_values.target_voltage / 1000, 1)
        current_values_dict["current_limit_mA"] = all_values.target_current
        current_values_dict["output_on"] = 1 if all_values.output_is_on else 0

        return json.dumps(current_values_dict)

    def get_current(self):
        """Get the output current of the connected device

        :return: str -- The output current in mA. Empty string if no device is connected
        """

        if not self._hardware_interface.connect():
            return ""
        try:
            all_values = self._hardware_interface.get_all_values()
        except PsControllerException:
            return ""
        return str(all_values.output_current)

    def get_voltage(self):
        """Get the voltage output of the connected device.

        :return: str -- The output voltage in V. Empty string if no device is connected
        """
        if not self._hardware_interface.connect():
            return ""
        try:
            all_values = self._hardware_interface.get_all_values()
        except PsControllerException:
            return ""
        return str(round(all_values.output_voltage / 1000, 1))

    def get_output_on(self):
        """Get if output of the connected device is on

        :return: bool -- If output is on or not
        """
        self._hardware_interface.connect()
        try:
            all_values = self._hardware_interface.get_all_values()
        except PsControllerException:
            return ""
        return all_values.output_is_on

    def set_device_on(self):
        """Sets output of connected device on

        :return: None
        """
        self._hardware_interface.connect()
        try:
            self._hardware_interface.set_output_on(True)
        except PsControllerException:
            pass

    def set_device_off(self):
        """Sets output of connected device off

        :return: None
        """
        self._hardware_interface.connect()
        try:
            self._hardware_interface.set_output_on(False)
        except PsControllerException:
            pass

    def connect(self):
        """Tries to connect to a DPS201

        :return: bool -- If connecting to a device was successful
        """
        if self._hardware_interface.connected():
            return True
        return self._hardware_interface.connect()

    def connected_json(self):
        """Gets connection status and possible authentication issues

        :return: str -- JSON dict with the following keys
            - connected
            - authentication_error
        """
        connected = self._hardware_interface.connect()
        return_value = dict()
        return_value["connected"] = 1 if connected else 0
        return_value["authentication_error"] = 0 if connected else (1 if self._authentication_errors() else 0)
        return json.dumps(return_value)

    def _authentication_errors(self):
        return self._hardware_interface.authentication_errors_on_machine()