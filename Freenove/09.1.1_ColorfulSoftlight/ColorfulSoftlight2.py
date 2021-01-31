#!/usr/bin/env python3
#############################################################################
# Filename    : Softlight.py
# Description : Control RGBLED with Potentiometer
# Author      : Rosario Paolella
# modification: 2021/01/29
########################################################################
import RPi.GPIO as GPIO
from ADCDevice import *
from gpiozero import RGBLED
from colorzero import Color
from guizero import *
import time

###########Start Functions############################################### 
def StartProcess():
    global processActive
    processActive=True

def EndProcess():
    global processActive
    processActive=False

def on_resize(event):
     DrawColorbox(event.width,event.height)

def Clean():
    adc.close()
    GPIO.cleanup()

#Draw Colored Circle in the middle of color box
def DrawColorbox(width,height):
    global colorRead
    global currentWidth,currentHeight

    currentWidth=width
    currentHeight=height

    #draw a circle with size equal to minimun with, height of the container with 10 pixel border  
    if (width>height)  : 
        diametro=height -10
    else :
        diametro=width-10
    
    #calculate the x of the start point 
    x1=width/2 - diametro/2
    #calculate the y of the start point 
    y1=height/2-diametro /2

    drawing.clear()
    drawing.oval(x1,y1, x1+diametro, y1+diametro,colorRead.html, outline=False, outline_color="black")


   
def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)


def ProcessData():
    global processActive
    global colorRead
      
    if(processActive):
        value_Red = adc.analogRead(0)       # read ADC value of 3 potentiometers
        value_Green = adc.analogRead(1)
        value_Blue = adc.analogRead(2)

        colorRead=Color (value_Red,value_Green,value_Blue)

        #set read values on label on the screen  
        red_value.value=value_Red
        green_value.value=value_Green
        blue_value.value=value_Blue

        led.color = Color(value_Red,value_Green,value_Blue) #set color

        DrawColorbox(currentWidth,currentHeight)
    else:
        #set N/A values on label on the screen  
        red_value.value="N/A"
        green_value.value="N/A"
        blue_value.value="N/A"
############ END FUNCTIONS###############################################



###################START APPLICATION###############################################

app = App(title="Control RGBLED with Potentiometer ")
colorRead=Color(100,100,100)

#current width and height of the color box used to draw circle in the middle
currentWidth=0
currentHeight=0

#true start read, false stop read
processActive=False

adc = ADCDevice() # Define an ADCDevice class object
led = RGBLED(22, 27,17,False)

setup()

#Gui Design#################################################
title_box = Box(app, width="fill", align="top")

#####Box with Read values
values_box = Box(app,  width="fill", height="fill",align="top")

red_box=Box(values_box,align="left", width="fill")
Text(red_box,text="RED",color="red",size=16, align="top", width="fill")
red_value=Text(red_box, text="N/A",size=16,align="bottom", width="fill")

green_box=Box(values_box,align="left", width="fill")
Text(green_box,text="GREEN",color="green",size=16 ,align="top", width="fill")
green_value=Text(green_box,  text="N/A",size=16,align="bottom", width="fill")

blue_box=Box(values_box,align="right", width="fill")
Text(blue_box,text="BLUE",color="blue",size=16, align="top", width="fill")
blue_value=Text(blue_box, text="N/A",size=16,align="bottom", width="fill")

#####Box with Resuling Color
color_box = Box(app, width="fill", align="top",border=True)
#use tk to add on_resize event
color_box.tk.bind('<Configure>', on_resize) 

drawing = Drawing(color_box,width="fill",height="fill")

#####Box with Button
buttons_box = Box(app, width="fill", align="bottom")
buttonOK = PushButton(app, command=StartProcess, text="Start",align="left",width="fill")
buttonCancel= PushButton(app, command=EndProcess,text="Stop", align="right",width="fill")

app.repeat(50,ProcessData)

app.display()
app.when_closed= Clean()