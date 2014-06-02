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
        self._hardware_interface.connect()
        if self.connected():
            self._hardware_interface.start_streaming()
            self._initialize_streaming_values()
            self._start_fetching_stream_values()

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

    def get_values(self) -> DeviceValues:
        """
        Returns the current device values of the PS201. Raises a serial.Serial exception if not connected
        """
        if not self._hardware_interface.connect():
            return
        return self._hardware_interface.get_all_values()

    def get_current_json(self) -> str:
        """
        Get a JSON object that represents the current device state
        """
        if not self._hardware_interface.connect():
            return ""
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

    def _add_all_values_to_json(self, all_values: DeviceValues):
        """
        Add values to dict. Also make sure only 1000 items are in each list to avoid memory overflow
        """
        self._all_values_dict["voltage"]["datasets"][0]["data"].append(all_values.target_voltage)
        self._all_values_dict["voltage"]["labels"].append("")
        self._all_values_dict["current"]["datasets"][0]["data"].append(all_values.target_current)
        self._all_values_dict["current"]["labels"].append("")


        items_to_store = 1000
        number_of_items = len(self._all_values_dict["voltage"]["datasets"][0]["data"])
        if number_of_items > items_to_store:
            self._all_values_dict["voltage"]["datasets"][0]["data"] =\
                self._all_values_dict["voltage"]["datasets"][0]["data"][number_of_items - items_to_store:]
            self._all_values_dict["voltage"]["labels"] = self._all_values_dict["voltage"]["labels"][number_of_items - items_to_store:]
            self._all_values_dict["current"]["datasets"][0]["data"] = \
                self._all_values_dict["current"]["datasets"][0]["data"][number_of_items - items_to_store:]
            self._all_values_dict["current"]["labels"] = self._all_values_dict["current"]["labels"][number_of_items - items_to_store:]

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

    def _initialize_streaming_values(self):
        self._all_values_dict["voltage"] = dict()
        self._all_values_dict["voltage"]["datasets"] = [{"data": []}]
        self._all_values_dict["voltage"]["datasets"][0]["strokeColor"] = "rgba(151,232,40,1)"
        self._all_values_dict["voltage"]["labels"] = []
        self._all_values_dict["current"] = dict()
        self._all_values_dict["current"]["datasets"] = [{"data": []}]
        self._all_values_dict["current"]["datasets"][0]["strokeColor"] = "rgba(48,200,227,1)"
        self._all_values_dict["current"]["labels"] = []

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