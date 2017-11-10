"""
Forms the bytearray message to write raw RGB values to each LED on the LED ring
"""

from homeboy.messages import message_type
from homeboy.messages.base_message import BaseMessage


class MessageSetRawValues(BaseMessage):

    def __init__(self, data=bytearray(72)):
        super(MessageSetRawValues, self).__init__(message_type.MSG_SET_RAW_VALUES, data)
