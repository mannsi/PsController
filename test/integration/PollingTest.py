"""
This is an integration test script. It tests every voltage value from 0V - 8V by going through
increments of 0.1 V for a low target current. Then it sets a low voltage and goes through set current of
0 - 1000 mA. In this second run the goal is simply to see if every set value is correct and that
communication between device and computer behaves as expected.

The test condition are
- target voltage and current are the same as what was set
- output voltage is closer to the set values then a predefined deviation

Preconditions:
- DPS201 is connected to the computer via usb
- DPS201 is powered on and with input voltage 12V
"""

import time
import unittest

from ps_controller.protocol.ProtocolFactory import ProtocolFactory
from ps_controller.DeviceValues import DeviceValues


MAX_VOLTAGE_PERCENTAGE_DEVIATION = 0.02
MAX_VOLTAGE_ABSOLUTE_DEVIATION = 0.21

MAX_CURRENT_PERCENTAGE_DEVIATION = 0.02
MAX_CURRENT_ABSOLUTE_DEVIATION = 21

MAX_VOLTAGE_TEST_RANGE = 8

TARGET_CURRENT = 10
SLEEP_BETWEEN_STEPS = 2


class PollingTest(unittest.TestCase):
    def setUp(self):
        self._hardware_interface = ProtocolFactory().get_protocol("usb")
        connected = self._hardware_interface.connect()
        if not connected:
            raise Exception("Unable to connect to PS201")
        self._hardware_interface.set_target_voltage(0)
        self._hardware_interface.set_target_current(0)

        self._hardware_interface.set_device_is_on(True)

    def tearDown(self):
        self._hardware_interface.set_target_voltage(0)
        self._hardware_interface.set_target_current(0)
        self._hardware_interface.set_device_is_on(False)

    def test_voltage(self):
        """
        Test the range of a voltage values with a current value of TARGET_CURRENT
        """
        voltage_values = [x / 10 for x in range(int(MAX_VOLTAGE_TEST_RANGE * 10))]
        for v in voltage_values:
            self._compare_value_set(TARGET_CURRENT, v)
        print("Test script ran successfully")

    def _test_current(self):
        """
        Test the range of current values with voltage value of 1V
        """
        for c in range(10, 1000, 10):
            self._compare_value_set(c, 1)
        print("Test script ran successfully")

    def _compare_target_and_output_values(self, target_voltage: float, target_current: int, all_values: DeviceValues):
        if not self._current_within_bounds(target_current, all_values.output_current):
            self._raise_exception(target_current, all_values.output_current, "Current")
        if not self._voltage_within_bounds(target_voltage, all_values.output_voltage/1000):
            self._raise_exception(target_voltage, all_values.output_voltage, "Voltage")

    def _voltage_within_bounds(self, target, measured):
        return abs(target - measured) <= max(MAX_VOLTAGE_ABSOLUTE_DEVIATION, MAX_VOLTAGE_PERCENTAGE_DEVIATION * target)

    def _current_within_bounds(self, target, measured):
        return abs(target - measured) <= max(MAX_CURRENT_ABSOLUTE_DEVIATION, MAX_CURRENT_PERCENTAGE_DEVIATION * target)

    def _raise_exception(self, target, measured, value_name: str):
        raise Exception(value_name + " not correct. Target: " + str(target) + " but measure: " + str(measured))

    def _compare_value_set(self, target_current, target_voltage):
        """Sets the values of the device to target values and then records the device output values.
        Finally compares these values and throws an exception if they do not match according to expectations"""
        print("Checking voltage: ", target_voltage, " and current: ", target_current)
        self._hardware_interface.set_target_voltage(target_voltage*1000)
        self._hardware_interface.set_target_current(target_current)
        time.sleep(SLEEP_BETWEEN_STEPS)
        all_values = self._hardware_interface.get_all_values()

        if target_current != all_values.target_current:
            raise Exception("Wrong target current measured. Target current is ", target_current,
                            " but measured target current is ", all_values.target_current)
        if target_voltage != all_values.target_voltage/1000:
            raise Exception("Wrong target voltage measured. Target voltage is ", target_voltage,
                            " but measured target voltage is ", all_values.target_voltage/1000)
        self._compare_target_and_output_values(target_voltage, target_current, all_values)


if __name__ == "__main__":
    unittest.main()
