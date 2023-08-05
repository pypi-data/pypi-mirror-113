# -*- coding:utf-8 -*-
from __future__ import print_function
import RPi.GPIO as GPIO


class Light(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(33, GPIO.IN)

    @staticmethod
    # false means shiny
    def shiny_or_dark():
        input_value = GPIO.input(33)
        return input_value


if __name__ == "__main__":
    light = Light()
    print(light.shiny_or_dark())
