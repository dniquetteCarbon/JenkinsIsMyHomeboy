import os
import serial
import time
import logging

LOG = logging.getLogger(__name__)

class HomeboySerial():
    def __init__(self, baud_rate=None, port=None):
        """
        Creates an instance of s seri
        :param baud_rate:
        :param port:
        """
        self.baud_rate = baud_rate or 115200
        self.port = port or os.environ.get('SERIAL_PORT')
        LOG.info("Opening a Serial connection to %s at %s baud.", self.port, self.baud_rate)
        self.serial_conn = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=0.5)

    def write_to_serial(self, data):
        """
        :param data: bytearray with formatted header and footer to write to device
        :return: None
        """

        self.serial_conn.write(data)
        time.sleep(0.01)