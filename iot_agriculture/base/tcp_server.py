from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory as ServFactory
from typing import Dict, Callable
from iot_agriculture import Connection
import logging


class TcpServer(ServFactory):
    def __init__(self, host: str, port: int, log_path: str, name: str, callbacks: dict, *args, **kwargs):
        super(TcpServer, self).__init__(*args, **kwargs)
        self.port = port
        self.name = name
        self.logger = logging.getLogger("tcp_server")
        self.callbacks: Dict[str, Callable] = callbacks
        self.listener = None
        self.host = host

    def buildProtocol(self, addr):
        return Connection(self.callbacks, self.logger, self.name)

    def start(self):
        self.listener = reactor.listenTCP(self.port, self)
        self.logger.info(f"Listening to {self.host}:{self.port}")

    def stop(self):
        self.listener.stopListening()


if __name__ == '__main__':
    # server = ServerFactory()

    # server.start()
    # server.startFactory()
    reactor.run()
