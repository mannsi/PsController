from ..DeviceValues import DeviceValues
from ..connection.BaseConnectionInterface import BaseConnectionInterface


class BaseDeviceInterface:
    """An interface to a device"""
    def connect(self):
        """ Try to connect to a device

        :return: bool -- If connection was successful
        """
        raise NotImplementedError()

    def connected(self):
        """Returns if currently connected to a device

        :return: bool -- If connected
        """
        raise NotImplementedError()

    def authentication_errors_on_machine(self):
        """Returns if machine has trouble connecting to devices because of authentication issues

        :return: bool -- If there are authentication errors on machine
        """
        raise NotImplementedError()

    def get_all_values(self):
        """Returns the current values of the connected device

        :return: DeviceValues --
        :raise: PsControllerException
        """
        raise NotImplementedError()

    def set_target_voltage(self, voltage):
        """Set the target voltage of the connected device

        :param voltage: The voltage to set in mV
        :type voltage: int
        :return: None
        :raise: PsControllerException
        """
        raise NotImplementedError()

    def set_target_current(self, current):
        """Set the target current of the connected device

        :param current: The current to set in mA
        :type current: int
        :return: None
        :raise: PsControllerException
        """
        raise NotImplementedError()

    def set_output_on(self, is_on):
        """Set if output on connected device is on or off

        :param is_on: Whether output should be set on or off
        :type is_on: bool
        :return: None
        :raise: PsControllerException
        """
        raise NotImplementedError()
