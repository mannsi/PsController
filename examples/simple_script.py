from ps_controller.protocol.ProtocolFactory import ProtocolFactory
import sys
import time

hardware_interface = ProtocolFactory().get_protocol("usb")

if not hardware_interface.connected():
    connected = hardware_interface.connect()
    if not connected:
        print("Unable to connect to device")
        sys.exit()

hardware_interface.set_target_current(100)  # 100 mA current
hardware_interface.set_target_voltage(1000)  # 1V voltage
hardware_interface.set_device_is_on(True)  # Turn output on

time.sleep(0.5)

all_values = hardware_interface.get_all_values()
print(
    "Target current: {0}mA, Target voltage: {1}V, Output current: {2}mA, Output voltage: {3}V, Device is on: {4}".format(
        all_values.target_current,
        all_values.target_voltage / 1000,
        all_values.output_current,
        all_values.output_voltage / 1000,
        all_values.output_is_on))

hardware_interface.set_target_current(0)  # Cleanup
hardware_interface.set_target_voltage(0)  # Cleanup
hardware_interface.set_device_is_on(False)  # Turn output off
