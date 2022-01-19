from iot_agriculture import TcpServer
import logging

logger = logging.getLogger("Server")


class Server(object):
    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.server = TcpServer(self.config.get("host"),
                                self.config.get("port"),
                                callbacks={"on_connect": self.on_connect,
                                           "on_data": self.on_data,
                                           "on_disconnect": self.on_disconnect})

    @staticmethod
    def on_connect(connection):
        logger.info(f"New Connection")

    @staticmethod
    def on_data(connection, data):
        logger.info(data)

    @staticmethod
    def on_disconnect(connection, reason):
        logger.info("Client disconnected")
        logger.info(reason)

    def start(self):
        logger.info("server started")
        self.server.start()

    def stop(self):
        logger.info("server stopped")
        logger.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++\n")
        self.server.stop()
