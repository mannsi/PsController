import json
import logging
from apscheduler.scheduler import Scheduler


from ps_controller.protocol.ProtocolFactory import ProtocolFactory
from ps_controller.Constants import Constants
from ps_controller.DeviceValues import DeviceValues


class Wrapper:
    def __init__(self):
        self._stream_values_polling = Scheduler()
        self._all_values_dict = dict()
        self._logHandlersAdded = False
        self._set_logging(logging.DEBUG)
        self._hardware_interface = ProtocolFactory().get_protocol("usb")
        self._initialize_values()

    def set_voltage(self, voltage: float):
        """
        Set the voltage value of the connected PS201. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        self._hardware_interface.set_target_voltage(voltage)

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
        return json.dumps(self._all_values_dict)

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

    def start_streaming(self):
        self._hardware_interface.start_streaming()
        self._start_fetching_stream_values()

    def _add_all_values_to_json(self, all_values: DeviceValues):
        """
        Remove the first value from dicts and add the new values to the back of the lists
        """
        self._all_values_dict["voltage"]["datasets"][0]["data"].pop(0)
        self._all_values_dict["current"]["datasets"][0]["data"].pop(0)
        self._all_values_dict["voltage"]["datasets"][0]["data"].append(all_values.output_voltage)
        self._all_values_dict["current"]["datasets"][0]["data"].append(all_values.output_current)

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

    def _initialize_values(self):
        self._all_values_dict["voltage"] = dict()
        self._all_values_dict["voltage"]["datasets"] = [{"data": []}]
        self._all_values_dict["voltage"]["datasets"][0]["strokeColor"] = "rgba(151,232,40,1)"
        self._all_values_dict["voltage"]["labels"] = []
        self._all_values_dict["current"] = dict()
        self._all_values_dict["current"]["datasets"] = [{"data": []}]
        self._all_values_dict["current"]["datasets"][0]["strokeColor"] = "rgba(48,200,227,1)"
        self._all_values_dict["current"]["labels"] = []

        # TODO Try setting 
        for x in range(150):
            self._all_values_dict["voltage"]["datasets"][0]["data"].append(0)
            self._all_values_dict["voltage"]["labels"].append("")
            self._all_values_dict["current"]["datasets"][0]["data"].append(0)
            self._all_values_dict["current"]["labels"].append("")

    def _start_fetching_stream_values(self):
        # Start a timer that adds to the list of values
        self._stream_values_polling.start()
        self._stream_values_polling.add_interval_job(self._add_to_stream_values, seconds=0.1, args=[])

    def _add_to_stream_values(self):
        streaming_values = self._hardware_interface.get_current_streaming_values()
        if streaming_values:
            self._add_all_values_to_json(streaming_values)


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
        super()._add_all_values_to_json(mock_values)

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

    def start_streaming(self):
        pass
