from iot_agriculture import RaspberryPi, Config
from twisted.internet import reactor


def raspberrypi(input_args, config_location):
    config = Config(config_location)
    config.add_config(["raspberry_pi.yml"])
    pi = RaspberryPi(config)

    reactor.addSystemEventTrigger('before', 'shutdown', pi.stop)
    pi.start()
    reactor.run()
