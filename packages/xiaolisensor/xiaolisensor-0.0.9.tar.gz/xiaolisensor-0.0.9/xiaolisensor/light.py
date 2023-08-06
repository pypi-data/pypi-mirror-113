# -*- coding:utf-8 -*-
from __future__ import print_function
import RPi.GPIO as GPIO


class Light(object):
    def __init__(self):
        pass

    @staticmethod
    # false means shiny
    def shiny_or_dark():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.IN)
        input_value = GPIO.input(13)
        GPIO.cleanup()
        return input_value


if __name__ == "__main__":
    light = Light()
    print(light.shiny_or_dark())
