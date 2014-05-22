import glob

import serial

from .BaseConnectionInterface import BaseConnectionInterface
import ps_controller.utilities.OsHelper as osHelper
from ..Constants import *


class UsbConnection(BaseConnectionInterface):
    def __init__(
            self,
            baud_rate,
            timeout,
            logger,
            id_message,
            device_verification_func):
        self._baud_rate = baud_rate
        self._timeout = timeout
        self._logger = logger
        self._id_message = id_message
        self._device_verification_func = device_verification_func
        self._connection = None

    def connect(self):
        """
        Tries to connect to a PS201 via USB. Returns a bool indicating if connecting was successful
        """
        available_ports = self._available_connections()
        for port in available_ports:
            if self._device_on_port(port):
                self._connection = serial.Serial(port, self._baud_rate, timeout=self._timeout)
                break
        return self.connected()

    def disconnect(self):
        """
        Disconnects from the currently connected PS201.
        """
        self._connection.close()

    def connected(self):
        """
        Returns a bool value indicating if connected to PS201
        """
        if not self._connection:
            return False
        return self._connection.connected()

    def clear_buffer(self):
        """
        Clears the read buffer from the device.
        """
        if self.connected():
            self._connection.flushInput()

    def get(self):
        """
        Reads the values from PS201 and returns them. A single response from PS201 is surrounded with START characters
        If not connected, None is returned
        """
        if not self.connected():
            return None
        serial_response = self._read_device_response(self._connection)
        return serial_response

    def set(self, sending_data):
        """
        Sends sending_data to the connected PS201.
        """
        if not self.connected():
            return
        self._send_to_device(self._connection, sending_data)

    def _available_connections(self):
        """Get available usb ports"""
        system_type = osHelper.getCurrentOs()
        available = []
        usb_list = []
        if system_type == osHelper.WINDOWS:
            usb_list = range(256)
        elif system_type == osHelper.OSX:
            usb_list = glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
        elif system_type == osHelper.LINUX:
            usb_list = glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')

        for port in usb_list:
            try:
                con = serial.Serial(port, self._baud_rate, timeout=0.01)
                available.append(con.portstr)
                con.close()
            except serial.SerialException:
                pass
        return available

    def _send_to_device(self, serial_connection, data):
        serial_connection.write(data)

    def _read_device_response(self, serial_connection):
        return self._read_line(serial_connection)

    def _read_line(self, serial_connection):
        """Custom readLine method to avoid end of line char issues"""
        line = bytearray()
        start_count = 0
        while True:
            c = serial_connection.read(1)
            if c:
                line += c
            else:
                break

            if c[0] == START:
                start_count += 1
            if start_count == 2:
                break
        return bytes(line)

    def _device_on_port(self, usb_port):
        try:
            temp_connection = serial.Serial(usb_port, self._baud_rate, timeout=self._timeout)
            self._send_to_device(temp_connection, self._id_message)
            device_response = self._read_device_response(temp_connection)
            return self._device_verification_func(device_response)
        except:
            return False