#!/usr/bin/env python3
########################################################################
# Filename    : LightWater_Random.py
# Description : Use LEDBar Graph(10 LED)
# Author      : Rosario Paolella
# modification: 2021/17/01
########################################################################
from gpiozero import LEDBoard
from time import sleep
from signal import pause
from random import seed
from random import randint

print('Program is starting ... ')

value=0
precvalue=0

seed()
ledPins = ["J8:11","J8:12","J8:13","J8:15","J8:16","J8:18","J8:22","J8:3","J8:5","J8:24"]

leds = LEDBoard(*ledPins, active_high=False)

while True:
    precvalue=value
    value=randint(0,len(ledPins)-1)
    print ("Random Led On:" + str(value) + " Off:" + str(precvalue))
    leds.on(value)
    #leds.off(precvalue)
    sleep(1)