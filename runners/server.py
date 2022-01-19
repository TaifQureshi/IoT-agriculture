from iot_agriculture import Server, Config
from twisted.internet import reactor


def server(input_args, config_location):
    config = Config(config_location)
    config.add_config(["server.yml"])
    aws_server = Server(config)

    reactor.addSystemEventTrigger('before', 'shutdown', aws_server.stop)
    aws_server.start()
    reactor.run()
