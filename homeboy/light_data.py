"""
Object for easy interaction with the LEDs
"""

class LightData:

    def __init__(self):
        self.num_lights = 24
        self.lights = []
        for _ in range(24):
            self.lights.append([0,0,0])

    def setPixelColor(self, pixel, r, g, b):
        """
        Sets the specified pixel to the given RGB value
        :param pixel: index of the LED to update
        :param r: Red value
        :param g: Green value
        :param b: Blue value
        :return: None
        """
        self.lights[pixel] = [r, g, b]

    def setAllColor(self, r, g, b):
        """
        Sets every pixel in the ring to the specified RBG color (useful for fades, flashes, etc.)
        :param r: Red value
        :param g: Green value
        :param b: Blue value
        :return:
        """
        for light in range(self.num_lights):
            self.lights[light] = [r, g, b]

    def getByterray(self):
        """
        Returns the bytearray formatted data associated with the light_data
        :return: bytearray of light data
        """
        single_array = []
        for light in self.lights:
            for color in light:
                single_array.append(color)
        return bytearray(single_array)

