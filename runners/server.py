from iot_agriculture import Server, base_setting
from twisted.internet import reactor


def server(input_args, config_location):
    config = base_setting(config_location, "server.yml")
    aws_server = Server(**config)

    reactor.addSystemEventTrigger('before', 'shutdown', aws_server.stop)
    aws_server.start()
    reactor.run()
