import unittest
from ps_controller import SerialException
from ps_controller.protocol.UsbProtocol import UsbProtocol
from ps_controller.DeviceValues import DeviceValues
from ps_controller.data_mapping.UsbDataMapping import UsbDataMapping
from ps_controller.Commands import *
from test.Mocks import MockConnection, MockLogger


class TestUsbConnection(unittest.TestCase):
    def setUp(self):
        self._connection_mock = MockConnection()
        self._test_protocol = UsbProtocol(self._connection_mock, MockLogger())

    def test_connecting_works(self):
        self._test_protocol.connect()
        self.assertTrue(self._test_protocol.connected(), "Should be connected after connecting")

    def test_disconnected_throws_errors(self):
        self._test_protocol.connect()
        self._test_protocol.disconnect()
        self.assertRaises(SerialException, self._test_protocol.get_all_values)
        self.assertRaises(SerialException, self._test_protocol.set_target_current, 0)
        self.assertRaises(SerialException, self._test_protocol.set_target_voltage, 0)
        self.assertRaises(SerialException, self._test_protocol.set_device_is_on, True)

    def test_connected_set_with_no_acknowledge_should_throw(self):
        self._test_protocol.connect()
        self.assertRaises(SerialException, self._test_protocol.set_target_current, 0)
        self.assertRaises(SerialException, self._test_protocol.set_target_voltage, 0)
        self.assertRaises(SerialException, self._test_protocol.set_device_is_on, True)

    def test_connected_get_no_data_should_throw(self):
        self._test_protocol.connect()
        self.assertRaises(SerialException, self._test_protocol.get_all_values)

    def test_set_illegal_values_should_throw(self):
        self._test_protocol.connect()
        self.assertRaises(SerialException, self._test_protocol.set_target_current, "a")
        self.assertRaises(SerialException, self._test_protocol.set_target_voltage, "b")
        get_binary_data_for_all_values()

    def test_getting_normal_values(self):
        self._test_protocol.connect()
        device_values, binary_device_values = get_binary_data_for_all_values()
        self._connection_mock.set_binary_buffer_data(binary_device_values)
        fetched_values = self._test_protocol.get_all_values()
        
        self.assertEquals(device_values.input_voltage, fetched_values.input_voltage)
        self.assertEquals(device_values.output_current, fetched_values.output_current)
        self.assertEquals(device_values.output_is_on, fetched_values.output_is_on)
        self.assertEquals(device_values.output_voltage, fetched_values.output_voltage)
        self.assertEquals(device_values.pre_reg_voltage, fetched_values.pre_reg_voltage)
        self.assertEquals(device_values.target_current, fetched_values.target_current)
        self.assertEquals(device_values.target_voltage, fetched_values.target_voltage)

    def test_getting_bad_values(self):
        self._test_protocol.connect()
        device_values, binary_device_values = get_binary_data_for_all_values()
        binary_device_values.pop()
        self._connection_mock.set_binary_buffer_data(binary_device_values)
        self.assertRaises(SerialException, self._test_protocol.get_all_values)

if __name__ == '__main__':
    unittest.main()


def get_binary_acknowledgement():
    serial_data = UsbDataMapping.to_serial(AcknowledgementCommand())
    return serial_data


def get_binary_data_for_all_values():
    """
    Returns a tuple (device_values, binary_data_for_device_values_with_acknowledgement)
    """
    all_values = DeviceValues()
    all_values.input_voltage = 1
    all_values.output_voltage = 2.5
    all_values.pre_reg_voltage = 3
    all_values.output_current = 100
    all_values.output_is_on = True
    all_values.target_current = 200
    all_values.target_voltage = 4

    data = (str(all_values.output_voltage) + ';' +
            str(all_values.output_current) + ';' +
            str(all_values.target_voltage) + ';' +
            str(all_values.target_current) + ';' +
            str(all_values.pre_reg_voltage) + ';' +
            str(all_values.input_voltage) + ';' +
            str(int(all_values.output_is_on)))
    serial_data = UsbDataMapping.to_serial(WriteAllValuesCommand(), data)
    acknowledgement_data = get_binary_acknowledgement()
    serial_data_with_ack = acknowledgement_data
    for s in serial_data:
        serial_data_with_ack.append(s)

    return (all_values, serial_data_with_ack)

