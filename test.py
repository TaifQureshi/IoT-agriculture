import sys
import Adafruit_DHT
import time


sensor = Adafruit_DHT.DHT11
while True:

    humidity, temperature = Adafruit_DHT.read_retry(sensor, 26)

    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    time.sleep(1)
