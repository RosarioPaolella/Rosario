#!/usr/bin/env python3
#############################################################################
# Filename    : Softlight.py
# Description : Termometer
# Author      : Rosario Paolella
# modification: 2021/01/29
########################################################################
import RPi.GPIO as GPIO
from ADCDevice import *
from colorzero import Color
from guizero import *
import math
import time

###########Start Functions############################################### 
def getTemp_X_Pointer (value,left,width,minTemp,maxTemp):
    unit_T=width/(maxTemp+abs(minTemp))
    temp_inc=value+abs(minTemp)
    return temp_inc*unit_T+left

def on_resize(event):
     DrawTermometer(event.width,event.height)

def Clean():
    adc.close()
    GPIO.cleanup()

#Draw Termometer in the middle of color box
def DrawTermometer(width,height):
    global currentWidth,currentHeight
    global temperature

    currentWidth=width
    currentHeight=height

    T_Canvas.clear()

    #termometer left at 1/8 of box width 
    T_Left=currentWidth/8
    #termometer box is 6/8 total with , single box is 1/6 of 6/8 total width
    T_Width=(6*currentWidth/8)/6 
    #termometer top at 3/8 of height
    T_Top=3*currentHeight/8
    #termometer height is 1/8 of box height 
    T_Height=currentHeight/8
    
    
    #Draw 6 rectangle of different colors
    box_colors = ["skyblue1","lightblue1","yellow2","gold2","dark orange","red"]
    T_Values = ["-20 °C","-10 °C","0 °C","10 °C","20 °C","30 °C","40 °C"]

    #Draw Termometer Boxes
    for i in range(1,7):
        T_Canvas.rectangle(T_Left+(i-1)*T_Width, T_Top, T_Left+i*T_Width, T_Top+T_Height, box_colors[i-1],
        True,"gray33")
        #add termometer marks (1 mark per degree)
        for j in range (0,10):
            if (j==0 ):
                if (i==3) : 
                    color_text="red"
                else:
                    color_text="black"
                
                T_Canvas.line(T_Left+(i-1)*T_Width+(j*T_Width/10),T_Top-T_Height*0.2,T_Left+(i-1)*T_Width+(j*T_Width/10),
                T_Top+T_Height+T_Height*0.2,"black",2)
                T_Canvas.text(T_Left+(i-1)*T_Width+(j*T_Width/10)-3, T_Top+(T_Height*0.3)*4, 
                T_Values[i-1],color_text,"arial black",10)
            else:
                T_Canvas.line(T_Left+(i-1)*T_Width+(j*T_Width/10),T_Top,T_Left+(i-1)*T_Width+(j*T_Width/10),
                T_Top+T_Height,"black",1)

                #last mark
                if (i==6 and j==9):
                    T_Canvas.line(T_Left+(i-1)*T_Width+((j+1)*T_Width/10),T_Top-T_Height*0.2,T_Left+(i-1)*T_Width+((j+1)*T_Width/10),
                        T_Top+T_Height+T_Height*0.2,"black",2)
                    T_Canvas.text(T_Left+(i-1)*T_Width+((j)*T_Width/10)-3, T_Top+(T_Height*0.3)*4, 
                        T_Values[i], "black","arial black",10)
        

    #pointer of temperature ad triangle red-line-triangle red
    pointer_X=getTemp_X_Pointer(temperature,T_Left,T_Width*6,-20,40)
    T_Canvas.triangle(pointer_X-10,T_Top,pointer_X,T_Top+10,pointer_X+10,T_Top,"green",True,"black")
    T_Canvas.triangle(pointer_X-10,T_Height+ T_Top,pointer_X,T_Top+T_Height-10,pointer_X+10,T_Height+ T_Top,"green",True,"black")


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

   
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
    global temperature

    value = adc.analogRead(0)        # read ADC value A0 pin
    voltage = value / 255.0 * 3.3        # calculate voltage
    Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
    tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
    temperature = tempK -273.15        # calculate temperature (Celsius)
    txtTemperature.value=truncate(temperature,3)
    temperature=truncate(temperature,3)

    DrawTermometer(currentWidth,currentHeight)
############ END FUNCTIONS###############################################


###################START APPLICATION###############################################

app = App(title="Thermometer")

#current width and height of the color box used to draw circle in the middle
currentWidth=0
currentHeight=0

temperature=0

adc = ADCDevice() # Define an ADCDevice class object

setup()

#Gui Design#################################################
title_box = Box(app, width="fill", align="top")

#######Box with Termometer Graphics
termometer_box = Box(app, width="fill", height="fill" , align="top",border=True)
#use tk to add on_resize event
termometer_box.tk.bind('<Configure>', on_resize) 

T_Canvas = Drawing(termometer_box,width="fill",height="fill")

#####Box with Textual Temperature
buttons_box = Box(app, width="fill", align="bottom")
Text(buttons_box, text="Temperature (C°)",align="left",width="fill",size=32)
txtTemperature= Text(buttons_box, text="N/A", align="right",width="fill",size=32)

app.repeat(50,ProcessData)

app.display()
app.when_closed= Clean()