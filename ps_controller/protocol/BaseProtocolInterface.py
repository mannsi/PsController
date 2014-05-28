from ..DeviceValues import DeviceValues
from ..connection.BaseConnectionInterface import BaseConnectionInterface


class BaseProtocolInterface:
    def __init__(self, connection: BaseConnectionInterface):
        self._connection = connection

    def connect(self) -> bool:
        """
        Tries to connect to PS201
        """
        raise NotImplementedError()

    def connected(self) -> bool:
        """
        Returns if connect to PS201
        """
        raise NotImplementedError()

    def get_all_values(self) -> DeviceValues:
        """
        Returns the current values of the connected PS201.
        Throws SerialException if not connected
        """
        raise NotImplementedError()

    def set_target_voltage(self, voltage: float):
        """
        Set the target voltage of the connected PS201.
        Throws SerialException if not connected
        """
        raise NotImplementedError()

    def set_target_current(self, current: int):
        """
        Set the target current of the connected PS201.
        Throws SerialException if not connected
        """
        raise NotImplementedError()

    def set_device_is_on(self, is_on: bool):
        """
        Set if connected PS201 is on or off
        Throws SerialException if not connected
        """
        raise NotImplementedError()

