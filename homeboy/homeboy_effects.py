import logging
from homeboy.homeboy_serial import HomeboySerial


class HomeboyEffects():
    def __init__(self):
        self.homeboy_serial = HomeboySerial()
        self.display_os = 'win'

    def write_serial_effect(self, method, data):
        data_to_write = {}
        data_to_write['method'] = method
        data_to_write['data'] = data

        self.homeboy_serial.write_to_serial(data_to_write)

    def show_result_effect(self, data):
        if data['result'].lower() == 'failure':
            self.show_failure_effect()
        elif data['result'].lower() == 'success':
            self.show_success_effect()
        elif data['result'].lower() == 'unstable':
            self.show_unstable_effect()

        self.show_donut(data)

    def show_failure_effect(self):
        logging.info('Displaying Failure')
        data_to_write = None
        self.homeboy_serial.write_to_serial(data_to_write)

    def show_success_effect(self, data):
        logging.info('Displaying Success')

    def show_unstable_effect(self, data):
        logging.info('Displaying Unstable')

    def show_donut(self, data):
        logging.info('Displaying Donut')

if __name__ == "__main__":
    effects = HomeboyEffects()
    effects.show_failure_effect()