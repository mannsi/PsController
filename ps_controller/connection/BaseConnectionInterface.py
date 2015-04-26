class BaseConnectionInterface:
    def connect(self):
        """Tries to connect to a device
        :return: bool -- Connection successful
        """
        raise NotImplementedError()

    def disconnect(self):
        """Disconnects from the currently connected device
        :return: None
        """
        raise NotImplementedError()

    def connected(self):
        """Checks if currently connected to a device
        :return: bool -- If connected or not
        """
        raise NotImplementedError()

    def get(self):
        """Reads a single response from device
        :return: bytes or None -- A single device response or None if got no response
        """
        raise NotImplementedError()

    def set(self, sending_data):
        """Sends data to the connected device
        :param sending_data: The sending data
        :type sending_data: bytes
        :return: None
        """
        raise NotImplementedError()

    def has_available_ports(self):
        """Returns if any ports are available on the machine

        :return: bool -- If any ports are available
        """
        raise NotImplementedError()
