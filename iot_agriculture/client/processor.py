from iot_agriculture import TcpClient
import logging

logger = logging.getLogger("raspberry_pi")


class RaspberryPi(object):
    def __init__(self, config):
        self.config: dict = config
        self.tcp_client = TcpClient(self.config.get("host"),
                                    self.config.get("port"),
                                    callbacks={"on_connect": self.on_connect,
                                               "on_data": self.on_data,
                                               "on_disconnect": self.on_disconnect})

        self.connection = None

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

    def stop(self):
        logger.info("Connection to server terminated")
        logger.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++")
        self.tcp_client.stop()
