class BaseConnectionInterface:
    def connect(self) -> bool:
        """
        Tries to connect to a PS201 via USB. Returns a bool indicating if connecting was successful
        """
        raise NotImplementedError()

    def disconnect(self):
        """
        Disconnects from the currently connected PS201.
        """
        raise NotImplementedError()

    def connected(self) -> bool:
        """
        Returns a bool value indicating if connected to PS201
        """
        raise NotImplementedError()

    def get(self) -> bytearray:
        """
        Reads a single response from PS201 and returns them. A single response from PS201 is surrounded
        with START characters. If not connected, raise serial.Serial exception

        Returns: bytearray
        """
        raise NotImplementedError()

    def set(self, sending_data: bytearray):
        """
        Sends sending_data to the connected PS201. If not connected, raise serial.Serial exception
        """
        raise NotImplementedError()

    def has_available_ports(self) -> bool:
        """
        Returns if any ports are available on the machine
        """
        raise NotImplementedError()
