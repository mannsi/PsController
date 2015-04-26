import glob
import serial
from .BaseConnectionInterface import BaseConnectionInterface
import ps_controller.utilities.OsHelper as osHelper
from ..logging.CustomLoggerInterface import CustomLoggerInterface


class UsbConnection(BaseConnectionInterface):
    def __init__(
            self,
            logger,
            serial_link_generator,
            handshake_message,
            device_verification_func,
            device_start_end_byte):
        """

        :param logger: Logger to log messages
        :type logger: CustomLoggerInterface
        :param serial_link_generator: function that returns serial connections
        :type serial_link_generator: lambda: SerialConnectionInterface()
        :param handshake_message: Serial package sent to device for handshake.
        :type handshake_message: bytes
        :param device_verification_func: Function used to verify handshake sent to device
        :type device_verification_func: lambda x: func(device_serial_response: bytes , usb_port: int) -> bool
        :param device_start_end_byte: The byte that should start and end all device communications
        :type device_start_end_byte: int
        :return: None
        """
        self._logger = logger
        self._serial_link_generator = serial_link_generator
        self._id_message = handshake_message
        self._device_verification_func = device_verification_func
        self._base_connection = serial_link_generator()
        self._connected = False
        self._device_start_end_byte = device_start_end_byte

    def connect(self):
        if self._connected:
            return True
        available_ports = self._available_usb_ports()
        for port in available_ports:
            if self._device_on_port(port):
                if self._base_connection.isOpen():
                    self._base_connection.close()
                self._base_connection.port = port
                self._base_connection.open()
                self._connected = self._base_connection.isOpen()
                break
        return self._connected

    def disconnect(self):
        self._connected = False
        self._base_connection.close()

    def connected(self):
        return self._connected

    def get(self):
        try:
            serial_response = self._read_device_response(self._base_connection)
            return serial_response
        except serial.SerialException:
            self._connected = False

    def set(self, sending_data):
        try:
            self._send_to_device(self._base_connection, sending_data)
        except serial.SerialException:
            self._connected = False

    def has_available_ports(self):
        usb_ports_range = self._usb_port_range()
        for port in usb_ports_range:
            try:
                tmp_connection = self._serial_link_generator()
                tmp_connection.port = port
                tmp_connection.open()
                tmp_connection.close()
                return True
            except serial.SerialException:
                pass
        return False

    def _available_usb_ports(self):
        """Get list of available usb ports

        :return: list[str|int] -- List of available ports. Contains port name or port number
        """
        available = []
        usb_ports = self._usb_port_range()
        for port in usb_ports:
            try:
                tmp_connection = self._serial_link_generator()
                tmp_connection.port = port
                tmp_connection.open()
                available.append(tmp_connection.port)
                tmp_connection.close()
            except serial.SerialException:
                pass
        return available

    def _read_device_response(self, serial_connection):
        """Gets serial response from connected device

        :param serial_connection: The serial connection to the device
        :type serial_connection: SerialConnectionInterface
        :return: bytes -- Serial response from device
        """
        line = bytearray()
        start_count = 0
        while True:
            c = serial_connection.read(1)
            if c:
                line += c
            else:
                break

            if c[0] == self._device_start_end_byte:
                start_count += 1
            if start_count == 2:
                break
        return bytes(line)

    def _device_on_port(self, usb_port):
        """Checks if device is on the given port

        :param usb_port: The port to check on
        :type usb_port: str or int
        :return: If device was found on port
        """
        tmp_connection = self._serial_link_generator()
        tmp_connection.port = usb_port
        try:
            tmp_connection.open()
            self._send_to_device(tmp_connection, self._id_message)
        except serial.SerialException:
            return False
        self._logger.log_debug("Sending handshake data on port " + str(usb_port))
        device_serial_response = self._read_device_response(tmp_connection)
        tmp_connection.close()
        return self._device_verification_func(device_serial_response, usb_port)

    @staticmethod
    def _usb_port_range():
        """Gets typical USB port ranges for each OS

        :return: list[int|str] -- List of usb port numbers or names
        """
        system_type = osHelper.get_current_os()
        usb_ports = []
        if system_type == osHelper.WINDOWS:
            usb_ports = range(256)
        elif system_type == osHelper.OSX:
            usb_ports = glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
        elif system_type == osHelper.LINUX:
            usb_ports = glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')
        return usb_ports

    @staticmethod
    def _send_to_device(serial_connection, data):
        """Send data to device on serial_connection

        :param serial_connection: Serial connection that device is on
        :type serial_connection: SerialConnectionInterface
        :param data: Serial data to send
        :type data: bytes
        :return: None
        """
        serial_connection.write(data)
