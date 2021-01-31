#!/usr/bin/env python3
########################################################################
# Filename    : Doorbell3.py
# Description : Make doorbell with buzzer and button
# Author      : Rosario Paolella
# modification: 2021/01/23
########################################################################
from gpiozero import Button
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from signal import pause
from time import sleep

print ('Program is starting...')

TBuzzer = TonalBuzzer(17)
button = Button(18)

#b.play(Tone("A4")) #play A4 note
#b.play(Tone(220.0)) # Hz
#b.play(Tone(60)) # middle C in MIDI notation


def onButtonPressed():
    print("Button is pressed, Play Melody")
    TBuzzer.play("C4")
    sleep(0.5)
    TBuzzer.play("D4")
    sleep(0.5)
    TBuzzer.play("E4")
    sleep(0.5)
    TBuzzer.play("F4")
    sleep(1)
    TBuzzer.play("E4")
    sleep(0.5)
    TBuzzer.play("D4")
    sleep(0.5)
    TBuzzer.play("C4")
    sleep(1)
    TBuzzer.stop()
    print("Melody End>>")

def onButtonReleased():
    TBuzzer.stop()
    print("Button is released, Stop Play<<<")

button.when_pressed = onButtonPressed
button.when_released = onButtonReleased

pause()
