from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from typing import Dict, Callable
from iot_agriculture import get_logger, Connection


class ClientFactory(ClFactory):
    def __init__(self, name: str, log_path: str,
                 host: str, port: int, callbacks: Dict[str, Callable],
                 *args, **kwargs):
        super(ClientFactory, self).__init__(*args, **kwargs)
        self.port = port
        self.host = host
        self.callbacks = callbacks
        self.connector = None
        self.logger = get_logger(log_path, name)
        self.name = name

    def start(self):
        self.connector = reactor.connectTCP(
            self.host,
            self.port,
            self
        )

    def stop(self):
        self.connector.disconnect()

    def clientConnectionLost(self, connector, unused_reason):
        self.retry(connector)

    def clientConnectionFailed(self, connector, reason):
        self.retry(connector)

    def buildProtocol(self, addr):
        self.resetDelay()
        return Connection(self.callbacks, self.logger, self.name)


if __name__ == '__main__':
    def on_connect(connect):
        print(connect)
        # connect.send_data({"event": "subscribe", "symbol": "EURUSDm"})
        connect.send_data({"event": "candle_subscribe", "symbol": "EURUSDm", "time": "1_min"})

    def on_data(connect, data):
        print(data)


    def on_disconnect(connect, reason):
        print(reason)


    client = ClientFactory(name="test", log_path="D:\\Taif\\Forex_trading_bot\\logs",
                           host="localhost", port=8080, callbacks={"on_connect": on_connect,
                                                                   "on_data": on_data,
                                                                   "on_disconnect": on_disconnect})

    client.start()
    print("Clint Start")
    reactor.run()


