import logging
import time
import os
from homeboy.messages.message_set_raw_values import MessageSetRawValues
from homeboy import light_data

LOG = logging.getLogger(__name__)

class HomeboyEffects():
    def __init__(self, serial_session):
        self.serial_session = serial_session
        self.display_os = 'win'
        self.num_leds = int(os.environ.get("NUM_LEDS"))
        self.max_bright = int(os.environ.get("MAX_BRIGHTNESS"))
        self.max_green = int(self.max_bright - (self.max_bright * .75))
        self.max_red = self.max_bright
        self.blue_factor = 0


    def show(self, ldata: light_data.LightData):
        self.serial_session.write(MessageSetRawValues(ldata.getByterray()).get_message())
        time.sleep(.005)

    def create_donut(self, data):
        logging.info('Displaying Donut')
        ldata = light_data.LightData()

        fail_leds = 0 if data['fail'] == 0 else round(max(1, float(data['fail'])/data['total'] * self.num_leds))
        skip_leds = 0 if data['skip'] == 0 else round(max(1, float(data['skip'])/data['total'] * self.num_leds))
        pass_leds = self.num_leds - fail_leds - skip_leds

        led_index = 0
        for i in range(fail_leds):
            ldata.setPixelColor(led_index, self.max_red, 0, self.blue_factor)
            led_index += 1
        for i in range(skip_leds):
            ldata.setPixelColor(led_index, self.max_red, self.max_green, self.blue_factor)
            led_index += 1
        for i in range(pass_leds):
            ldata.setPixelColor(led_index, 0, self.max_green, self.blue_factor)
            led_index += 1

        self.show(ldata)

    def show_result_effect(self, data):
        self.blue_factor = 3 if self.display_os == 'win' else 0

        if data['result'].lower() == 'failure':
            self.show_failure_effect()
        elif data['result'].lower() == 'success':
            self.show_success_effect()
        elif data['result'].lower() == 'unstable':
            self.show_unstable_effect()

        # Sleep in between effects
        time.sleep(5)

        if data['result'].lower() == 'unstable':
            self.create_donut(data)


    def show_failure_effect(self):
        logging.info('Displaying Failure')
        self.flashing_effect()
        ldata = light_data.LightData()
        ldata.setAllColor(self.max_red,0,self.blue_factor)
        self.show(ldata)

    def show_success_effect(self):
        logging.info('Displaying Success')
        ldata = light_data.LightData()
        ldata.setAllColor(0,self.max_green,self.blue_factor)
        self.show(ldata)

    def show_unstable_effect(self):
        logging.info('Displaying Unstable')
        self.flashing_effect()
        ldata = light_data.LightData()
        ldata.setAllColor(self.max_red,self.max_green,self.blue_factor)
        self.show(ldata)

    def turn_off_all(self, ldata=light_data.LightData()):
        ldata.setAllColor(0,0,0)
        self.show(ldata)

    def flashing_effect(self, iterations=5):
        ldata = light_data.LightData()
        for _ in range(iterations):
            ldata.setAllColor(0,0,0)
            for i in range(0, self.num_leds, 2):
                ldata.setPixelColor(i, self.max_red, 0, 0)
            self.show(ldata)
            time.sleep(1)
            ldata.setAllColor(0,0,0)
            for i in range(1, self.num_leds, 2):
                ldata.setPixelColor(i,self.max_red, 0, 0)
            self.show(ldata)
            time.sleep(1)




if __name__ == "__main__":
    effects = HomeboyEffects()
    effects.show_failure_effect()