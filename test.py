import sys
import Adafruit_DHT
import time


sensor = Adafruit_DHT.DHT11
while True:
    print("taking temp")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 4)

    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    time.sleep(1)
