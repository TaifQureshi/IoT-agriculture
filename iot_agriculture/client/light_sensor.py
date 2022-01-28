import RPi.GPIO as GPIO
import logging
import random
logger = logging.getLogger("light_sensor")


class Light(object):
    def __init__(self, config):
        self.config = config
        self.pin = self.config.get("light_sensor")

    def set_sensor(self):
        GPIO.setup(self.pin, GPIO.IN)
        logger.info(f"LDR light sensor set at pin {self.pin}")

    def light_status(self):
        return not GPIO.input(self.pin)
        # return random.choice([True, False])
