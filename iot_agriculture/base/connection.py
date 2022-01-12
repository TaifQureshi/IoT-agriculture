from abc import ABC
from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import LineReceiver
import json


class Connection(LineReceiver):
    def __init__(self, callbacks: dict, logger, name: str = "TCP_Connection"):
        super(Connection, self).__init__()
        self.callbacks = callbacks
        self.logger = logger
        self.name = name

    def connectionMade(self):
        connect = self.callbacks.get("on_connect")
        if connect:
            connect(self)

    def lineReceived(self, data):
        receive = self.callbacks.get("on_data")
        if receive:
            receive(self, json.loads(data))

    def connectionLost(self, reason=connectionDone):
        disconnect = self.callbacks.get("on_disconnect")
        if disconnect:
            disconnect(self, reason)

    def send_data(self, data):
        if type(data) == str:
            self.sendLine(data.encode('utf-8'))
        elif type(data) == dict:
            self._send_data_json(data)
        else:
            raise TypeError("Only type of str of dict is required")

    def _send_data_json(self, data: dict):
        self.sendLine(json.dumps(data).encode('utf-8'))

    def rawDataReceived(self, data):
        pass
