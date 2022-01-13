from iot_agriculture import base_setting, RaspberryPi
from twisted.internet import reactor


def raspberrypi(input_args, config_location):
    config = base_setting(config_location, "raspberry_pi.yml")
    pi = RaspberryPi(config)

    reactor.addSystemEventTrigger('before', 'shutdown', pi.stop)
    pi.start()
    reactor.run()
