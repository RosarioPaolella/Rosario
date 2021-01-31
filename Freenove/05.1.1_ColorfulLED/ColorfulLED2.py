#!/usr/bin/env python3
########################################################################
# Filename    : BreathingLed2.py
# Description : breathing led with GPIOZero
# Author      : Rosario Paolella
# modification: 2021/01/21
########################################################################

from gpiozero import RGBLED
from colorzero import Color
from signal import pause
from random import seed
from random import randint
from time import sleep


print ('Program is starting ... ')

led = RGBLED(17, 18, 27,False)

r=randint(0,100)
g=randint(0,100)
b=randint(0,100)

r1=randint(0,100)
g1=randint(0,100)
b1=randint(0,100)


#blink
#led.blink(on_time=0.5, off_time=0.5, fade_in_time=0, fade_out_time=0, on_color=(r/100.0, g/100.0, b/100.0), off_color=(r1/100.0, g1/100.0, b1/100.0), n=None, background=True)

#fade
#led.pulse(fade_in_time=2, fade_out_time=2, on_color=(r/100.0, g/100.0, b/100.0), off_color=(r1/100.0, g1/100.0, b1/100.0), n=None, background=True)

while True:
    r=randint(0,100)
    g=randint(0,100)
    b=randint(0,100)

    led.color = Color(r,g,b) #set color

    print ('color is ',r,g,b)

    sleep(0.5)

pause()