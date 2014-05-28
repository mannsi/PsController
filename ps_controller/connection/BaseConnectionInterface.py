class BaseConnectionInterface:
    def connect(self) -> bool:
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def connected(self) -> bool:
        raise NotImplementedError()

    def clear_buffer(self):
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