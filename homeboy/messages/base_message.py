"""
Provides the header and footer for interfacing with the Arduino with LEDs
"""

class BaseMessage:

    def __init__(self, message_type: int, message_data: bytearray):
        self.message_type: int = message_type
        self.message_data: bytearray = message_data
        self.message_header: bytearray = bytearray([0xDE, 0xAD, 0xBE, 0xEF])
        self.message_footer: bytearray = bytearray([0xFE, 0xEB, 0xDA, 0xED])

    def get_message(self) -> bytearray:
        """
        Returns the fully formed message with header and footer
        :return: bytearray with message
        """
        message: bytearray = bytearray()
        message += self.message_header
        message += bytearray([self.message_type])
        message += self.message_data
        message += self.message_footer
        return message



