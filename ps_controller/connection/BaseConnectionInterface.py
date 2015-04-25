class BaseConnectionInterface:
    def connect(self):
        """Tries to connect to a PS201 via USB.
        :return: bool -- Connection successful
        """
        raise NotImplementedError()

    def disconnect(self):
        """Disconnects from the currently connected PS201.
        :return: None
        """
        raise NotImplementedError()

    def connected(self):
        """Checks if currently connected to a PS201
        :return: bool -- If connected or not
        """
        raise NotImplementedError()

    def get(self) -> bytearray:
        """Reads a single response from PS201
        :return: bytearray or None -- A single PS201 response or None if got no response
        """
        raise NotImplementedError()

    def set(self, sending_data: bytearray):
        """Sends data to the connected PS201
        :param sending_data: The sending data
        :type sending_data: bytearray
        :return: None
        """
        raise NotImplementedError()

    def has_available_ports(self):
        """Returns if any ports are available on the machine

        :return: bool -- If any ports are available
        """
        raise NotImplementedError()
