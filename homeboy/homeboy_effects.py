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

        num_set_leds = 0
        last_pixel = -1
        for _ in range(fail_leds):
            for pixel in reversed(range(num_set_leds, self.num_leds)):
                ldata.setPixelColor(pixel, self.max_red, 0, self.blue_factor)
                if last_pixel != -1 and last_pixel > num_set_leds:
                    ldata.setPixelColor(last_pixel, 0,0,0)
                last_pixel = pixel
                self.show(ldata)
                time.sleep(0.01)
            num_set_leds += 1

        for _ in range(skip_leds):
            for pixel in reversed(range(num_set_leds, self.num_leds)):
                ldata.setPixelColor(pixel, self.max_red, self.max_green, self.blue_factor)
                if last_pixel != -1 and last_pixel > num_set_leds:
                    ldata.setPixelColor(last_pixel, 0,0,0)
                last_pixel = pixel
                self.show(ldata)
                time.sleep(0.01)
            num_set_leds += 1

        for _ in range(pass_leds):
            for pixel in reversed(range(num_set_leds, self.num_leds)):
                ldata.setPixelColor(pixel, 0, self.max_green, self.blue_factor)
                if last_pixel != -1 and last_pixel > num_set_leds:
                    ldata.setPixelColor(last_pixel, 0,0,0)
                last_pixel = pixel
                self.show(ldata)
                time.sleep(0.01)
            num_set_leds += 1

    def show_result_effect(self, data):
        self.blue_factor = 3 if self.display_os == 'win' else 0

        if data['result'].lower() == 'failure':
            self.show_failure_effect()
        elif data['result'].lower() == 'success':
            self.show_success_effect()
        elif data['result'].lower() == 'unstable':
            self.show_unstable_effect()

        # Sleep in between effects
        # time.sleep(5)

        if data['result'].lower() == 'unstable' or data['result'].lower() == 'success':
            self.create_donut(data)


    def show_failure_effect(self):
        logging.info('Displaying Failure')
        self.flashing_effect()

    def show_success_effect(self):
        logging.info('Displaying Success')
        ldata = light_data.LightData()
        self.pulsing_effect(iterations=5, time_=5, r=0, g=self.max_green, b=self.blue_factor)

    def show_unstable_effect(self):
        logging.info('Displaying Unstable')
        self.pulsing_effect(iterations=5, time_=5, r=self.max_red, g=self.max_green, b=self.blue_factor)
        ldata = light_data.LightData()

    def pulsing_effect(self, iterations=5, time_=5, r=255, g=255, b=255):
        ldata = light_data.LightData()
        time_per_iteration = time_ / iterations
        steps_per_iteration = 50
        time_per_step = time_per_iteration / steps_per_iteration
        for _ in range(iterations):
            # fade in
            for i in range(int(steps_per_iteration / 2)):
                ldata.setAllColor(int(float(r) * i / (steps_per_iteration / 2)),
                                  int(float(g) * i / (steps_per_iteration / 2)),
                                  int(float(b) * i / (steps_per_iteration / 2)))
                self.show(ldata)
                time.sleep(time_per_step)
            # fade out
            for i in reversed(range(int(steps_per_iteration / 2))):
                ldata.setAllColor(int(float(r) * i / (steps_per_iteration / 2)),
                                  int(float(g) * i / (steps_per_iteration / 2)),
                                  int(float(b) * i / (steps_per_iteration / 2)))
                self.show(ldata)
                time.sleep(time_per_step)


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