from iot_agriculture import TcpClient
import logging
from twisted.internet import task
from datetime import time, datetime
import RPi.GPIO as GPIO
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
        self.check_task = task.LoopingCall(self.check)
        self.end_time = time(hour=12, minute=1)

    def config_gpio(self):
        pass

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
        self.check_task.start(self.config.get("interval"))

    def stop(self):
        logger.info("Connection to server terminated")
        logger.info("Stopping crop monitoring process")
        logger.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++\n")
        self.tcp_client.stop()

    def check(self):
        current_time = datetime.now()

        if current_time.hour == self.end_time.hour and current_time.minute == self.end_time.minute:
            self.stop()
        else:
            pass
