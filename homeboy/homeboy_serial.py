import os
import serial
import logging


# Header: 4 : 0xDE, 0xAD, 0xBE, x0EF
# Message Type: 1
# Message Data: X
# Footer: 4 : 0xFE, 0xEB, 0xDA, 0xED

RESULT_TYPE = 0
EFFECT_TYPE = 1
EFFECT_DATA_TYPE = 2


class HomeboySerial():
    def __init__(self):
        self.baud_rate = 9600
        self.port = os.environ.get('SERIAL_PORT')
        logging.info("Connection Name: %s", self.serial_conn.name)

    def write_to_serial(self, type, data):
        """
        :param type: method type
        :param data: method data
        :return:
        """
        #build byte array
        byte_data = data

        serial_conn = serial.Serial(port=self.port, baudrate=self.baud_rate)
        serial_conn.write(byte_data)
        serial_conn.close()
