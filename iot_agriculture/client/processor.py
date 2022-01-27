from iot_agriculture import TcpClient, SensorData, HeartBeat, Header, Logout
import logging
from twisted.internet import task
from datetime import time, datetime
# import RPi.GPIO as GPIO
from iot_agriculture.client import Light
from iot_agriculture.client import WaterController

logger = logging.getLogger("raspberry_pi")


# add * 60 to line 69

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
        self.heart_beat_task = task.LoopingCall(self.heart_beat)
        self.count = 0
        self.end_time = time(hour=12, minute=1)
        self.light_sensor = Light(self.config)
        self.last_water = None
        self.water_controller = WaterController(self.config)
        # self.config_gpio()
        self.water = False
        self.light = False
        self.data_status = {}

    # def config_gpio(self):
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setwarnings(False)
    #     self.light_sensor.set_sensor()
    #     self.water_controller.set_sensor()

    def on_connect(self, connection):
        logger.info("Connected to server")
        self.connection = connection
        if len(self.data_status) > 1:
            logger.info("sending backlog data to server")
            for uuid,data in self.data_status.items():
                self.connection.send_data(data.to_json())

    def on_disconnect(self, connection, reason):
        logger.error(reason)
        self.connection = None

    def on_data(self, connection, data):
        header = Header.de_json(data)
        data = header.payload
        if header.payload_type == "Responce":
            if data.received_uuid in self.data_status.keys():
                self.data_status.pop(data.received_uuid)

    def start(self):
        logger.info("Tying to connect to server")
        self.tcp_client.start()
        logger.info(f"Starting the crop status check task with the interval of {self.config.get('interval')} second")
        logger.info(f"Send data to server at interval of {self.config.get('send_data')} minutes")
        self.water_controller.start()
        self.check_task.start(int(self.config.get("interval")))
        self.send_data_task.start(int(self.config.get("send_data")))
        self.heart_beat_task.start(int(self.config.get("heart_beat")))

    def stop(self):
        logger.info("Connection to server terminated")
        logger.info("Stopping crop monitoring process")
        self.water_controller.stop()
        self.heart_beat_task.stop()
        header = Header("Logout", Logout(self.unique_id))
        self.connection.send_data(header.to_json())
        logger.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++\n")
        self.tcp_client.stop()
        # GPIO.cleanup()

    def check(self):
        current_time = datetime.now()

        if current_time.hour == self.end_time.hour and current_time.minute == self.end_time.minute:
            self.stop()
        else:
            self.light = self.light_sensor.light_status()
            self.water, self.last_water = self.water_controller.water_status()

    def send_data(self):
        time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        data = SensorData(light=self.light, water=self.water, client_id=self.unique_id, time=time,
                          last_water=self.last_water)
        header = Header("SensorData", data)
        self.data_status[header.uuid] = header
        if self.connection:
            self.connection.send_data(header.to_json())

    def heart_beat(self):
        data = HeartBeat(self.unique_id, self.count)
        if self.connection:
            header = Header("HeartBeat", data)
            self.connection.send_data(header.to_json())
        self.count += 1
