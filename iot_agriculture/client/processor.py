from iot_agriculture import TcpClient, SensorData, HeartBeat
import logging
from twisted.internet import task
from datetime import time, datetime
import RPi.GPIO as GPIO
from iot_agriculture.client import Light
from iot_agriculture.client import WaterController
from datetime import datetime
logger = logging.getLogger("raspberry_pi")


# add stop process before 12 pm daily to update

class RaspberryPi(object):
    def __init__(self, config):
        self.config: dict = config
        self.tcp_client = TcpClient(self.config.get("host"),
                                    self.config.get("port"),
                                    callbacks={"on_connect": self.on_connect,
                                               "on_data": self.on_data,
                                               "on_disconnect": self.on_disconnect})

        self.connection = None
        self.unique_id = self.config.get("unique_id")
        self.check_task = task.LoopingCall(self.check)
        self.send_data_task = task.LoopingCall(self.send_data)
        self.count = 0
        self.end_time = time(hour=12, minute=1)
        self.light_sensor = Light(self.config)
        self.water_controller = WaterController(self.config)
        self.config_gpio()
        self.water = False
        self.light = False

    def config_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.light_sensor.set_sensor()
        self.water_controller.set_sensor()

    def on_connect(self, connection):
        logger.info("Connected to server")
        self.connection = connection

    def on_disconnect(self, connection, reason):
        logger.error(reason)
        self.connection = None

    @staticmethod
    def on_data(connection, data):
        logger.info(data)

    def start(self):
        logger.info("Tying to connect to server")
        self.tcp_client.start()
        logger.info(f"Starting the crop status check task with the inter of {self.config.get('interval')}")
        self.water_controller.start()
        self.check_task.start(self.config.get("interval"))
        self.send_data_task.start(self.config.get("send_data"))

    def stop(self):
        logger.info("Connection to server terminated")
        logger.info("Stopping crop monitoring process")
        logger.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++\n")
        self.water_controller.stop()
        self.tcp_client.stop()
        GPIO.cleanup()

    def check(self):
        current_time = datetime.now()

        if current_time.hour == self.end_time.hour and current_time.minute == self.end_time.minute:
            self.stop()
        else:
            self.light = self.light_sensor.light_status()
            self.water = self.water_controller.water_status()

    def send_data(self):
        time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        data = SensorData(light=self.light, water=self.water, client_id=self.unique_id, time=time)
        if self.connection:
            self.connection.send_data(data.to_json())

    def heart_beat(self):
        data = HeartBeat(self.unique_id, self.count)
        if self.connection:
            self.connection.send_data(data.to_json())
        self.count += 1


