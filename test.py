# import sys
# import Adafruit_DHT
# import time
#
#
# sensor = Adafruit_DHT.DHT11
# while True:
#     print("taking temp")
#     humidity, temperature = Adafruit_DHT.read(sensor, 26)
#
#     print(f'Temp: {temperature} C  Humidity: {humidity} %')
#     time.sleep(3)

import RPi.GPIO as GPIO
import time


pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setup(pin, GPIO.IN)
#
# while True:
#     if not GPIO.input(pin):
#         print("water detected")
#     else:
#         print("no water")
#
#     time.sleep(1)

GPIO.setup(pin, GPIO.OUT)

print("motor start")
GPIO.output(pin, True)
time.sleep(5)
print("motor stop")
GPIO.output(pin, False)
GPIO.cleanup()
