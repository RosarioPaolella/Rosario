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

print('Program is starting ... ')

numberToConvert=512

ledPins = ["J8:11","J8:12","J8:13","J8:15","J8:16","J8:18","J8:22","J8:3","J8:5","J8:24"]

leds = LEDBoard(*ledPins, active_high=False)

#define array of 10 bit : 0000000000
binary = []
for i in range(10):
    binary.append(0)

print ("Init bit array:" + str(binary))

#convert number in binary string
number=numberToConvert
i=len(binary)-1

while number>0 :
    bit=number%2
    binary[i]=bit
    number=number//2
    i=i-1

print ("Decimal is "+ str(numberToConvert) + " Binary is :" + str(binary))


for i in range (len(binary)-1,-1,-1):
    if binary[i]==1  :
        leds.on(i)
    else : 
        leds.off (i)
