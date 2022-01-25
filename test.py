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


#


def loop():
    # Going forwards
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)


def stop():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)


Motor1A = 20
Motor1B = 21
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

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)

print("motor start")
loop()
input()
print("motor stop")
stop()
GPIO.clean()
