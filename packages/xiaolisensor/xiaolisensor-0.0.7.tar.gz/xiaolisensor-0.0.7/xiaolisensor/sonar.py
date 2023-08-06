# -*- coding:utf-8 -*-
from __future__ import print_function
import board
import adafruit_hcsr04


class Sonar(object):
    def __init__(self):
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

    def get_distance(self):
        return self.sonar.distance


if __name__ == "__main__":
    sonar = Sonar()
    print(sonar.get_distance())