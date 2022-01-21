import sys
import Adafruit_DHT
import time


sensor = Adafruit_DHT.DHT11
while True:
    print("taking temp")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 4)

    print(f'Temp: {temperature} C  Humidity: {humidity} %')
    time.sleep(1)
