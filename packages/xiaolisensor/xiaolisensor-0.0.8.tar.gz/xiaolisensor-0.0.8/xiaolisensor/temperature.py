# -*- coding:utf-8 -*-
from __future__ import print_function

import time
import RPi.GPIO as GPIO
import dht11


class Temp_Hum(object):
    def __init__(self):
        GPIO.setwarnings(False)

    @staticmethod
    def get_temperature():
        GPIO.setmode(GPIO.BCM)
        # read data using pin 17
        instance = dht11.DHT11(pin=17)
        i = 0
        while i < 5:
            result = instance.read()
            if result.is_valid():
                GPIO.cleanup()
                return "{:.2f}".format(result.temperature)
            else:
                time.sleep(1)
                i = i + 1
        GPIO.cleanup()
        return -301

    @staticmethod
    def get_humidity():
        GPIO.setmode(GPIO.BCM)
        # read data using pin 17
        instance = dht11.DHT11(pin=17)
        i = 0
        while i < 5:
            result = instance.read()
            if result.is_valid():
                GPIO.cleanup()
                return "{:.2f}".format(result.humidity)
            else:
                time.sleep(1)
                i = i + 1
        GPIO.cleanup()
        return -301


if __name__ == "__main__":
    tempHum = Temp_Hum()
    print(tempHum.get_humidity())
