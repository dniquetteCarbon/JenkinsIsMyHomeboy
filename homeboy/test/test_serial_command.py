import serial
import time
from homeboy.messages.message_set_raw_values import MessageSetRawValues
from homeboy.light_data import LightData

def show():
    ser.write(MessageSetRawValues(ld.getByterray()).get_message())
    time.sleep(0.005)

ser = serial.Serial('COM4', 115200, timeout=0.5)
ld = LightData()
ser.write(MessageSetRawValues(ld.getByterray()).get_message())
time.sleep(1)

for _ in range(10):
    for i in range(ld.num_lights):
        ld.setAllColor(0,0,0)
        for j in range(8):
            ld.setPixelColor(((i + j) % ld.num_lights), 255 - 32*j, min(16*j,255), 0)
        show()
        time.sleep(0.05)

