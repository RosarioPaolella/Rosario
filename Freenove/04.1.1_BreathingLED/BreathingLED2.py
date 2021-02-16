#!/usr/bin/env python3
########################################################################
# Filename    : BreathingLED2.py
# Description : Breathing LED2
# Author      : Rosario Paolella
# modification: 2019/12/27
########################################################################
from gpiozero import PWMLED
import time

led = PWMLED(27)     # define the LedPin


def loop():
    while True:
        for dc in range(0, 100, 1):     # make the led brighter
            led.value=dc/100             # set dc value as the duty cycle
            time.sleep(0.01)
        time.sleep(1)
        for dc in range(100, -1, -1): # make the led darker
            led.value=dc/100             # set dc value as the duty cycle
            time.sleep(0.01)
        time.sleep(1)

def destroy():
    GPIO.cleanup() # Release all GPIO
 
if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
