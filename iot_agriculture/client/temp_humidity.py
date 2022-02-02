import Adafruit_DHT
import logging

logger = logging.getLogger("Temperature")


class Temperature(object):
    def __init__(self, config):
        self.config = config
        self.pin = self.config.get("temp_sensor")
        self.sensor = Adafruit_DHT.DHT11

    def set_sensor(self):
        logger.info(f"Temperature and Humidity sensor set at pin {self.pin}")

    def get_temp(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor, self.pin)
        if humidity and temperature:
            return humidity, temperature
        elif humidity and temperature is None:
            return humidity, 0.0
        elif humidity is None and temperature:
            return 0.0, temperature
        return 0.0, 0.0
