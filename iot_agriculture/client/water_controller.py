import RPi.GPIO as GPIO
import logging

logging = logging.getLogger("water_controller")


class WaterController(object):
    def __init__(self, config):
        self.config = config
        self.sensor = self.config.get("water_sensor")
        self.motor1 = self.config.get("motor1")
        self.motor2 = self.config.get("motor2")
        self.run = False

    def set_sensor(self):
        GPIO.setup(self.motor1, GPIO.OUT)
        GPIO.setup(self.motor2, GPIO.OUT)
        GPIO.setup(self.sensor, GPIO.IN)

        GPIO.add_event_detect(self.sensor, GPIO.BOTH, bouncetime=300)
        GPIO.add_event_callback(self.sensor, self.controller)

    def start_motor(self):
        GPIO.output(self.motor1, GPIO.HIGH)
        GPIO.output(self.motor2, GPIO.LOW)

    def stop_motor(self):
        GPIO.output(self.motor1, GPIO.LOW)
        GPIO.output(self.motor2, GPIO.LOW)

    def controller(self, channel):
        if not self.run:
            return
        if not GPIO.input(channel):
            logging.info("stop water motor")
            self.stop_motor()
        else:
            logging.info("start water motor")
            self.start_motor()

    def start(self):
        self.run = True

    def stop(self):
        self.run = False
        self.stop_motor()

    def water_status(self):
        return not GPIO.input(self.sensor)

