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


pin = 23
pin1 = 24
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
GPIO.setup(pin1, GPIO.OUT)
print("motor start")
GPIO.output(pin1, GPIO.HIGH)
GPIO.output(pin, GPIO.LOW)
input()
print("motor stop")
GPIO.output(pin1, GPIO.LOW)
GPIO.output(pin, GPIO.LOW)
GPIO.cleanup()
