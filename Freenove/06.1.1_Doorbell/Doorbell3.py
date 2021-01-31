#!/usr/bin/env python3
########################################################################
# Filename    : Doorbell3.py
# Description : Make doorbell with buzzer and button
# Author      : Rosario Paolella
# modification: 2021/01/23
########################################################################
from gpiozero import Buzzer, Button
from signal import pause

print ('Program is starting...')

led = Buzzer(17)
button = Button(18)

def onButtonPressed():
    led.on()
    print("Button is pressed, led turned on >>>")

def onButtonReleased():
    led.off()
    print("Button is released, led turned on <<<")

button.when_pressed = onButtonPressed
button.when_released = onButtonReleased

pause()
