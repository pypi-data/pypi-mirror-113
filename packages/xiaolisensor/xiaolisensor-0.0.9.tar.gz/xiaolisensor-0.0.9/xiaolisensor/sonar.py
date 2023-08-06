# -*- coding:utf-8 -*-
from __future__ import print_function
import board
import RPi.GPIO as GPIO
import adafruit_hcsr04


class Sonar(object):
    def __init__(self):
        pass

    @staticmethod
    def get_distance():
        GPIO.setmode(GPIO.BCM)
        sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
        dis = sonar.distance
        GPIO.cleanup()
        return dis


if __name__ == "__main__":
    sonar = Sonar()
    print(sonar.get_distance())