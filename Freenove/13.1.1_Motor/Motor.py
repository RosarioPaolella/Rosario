#!/usr/bin/env python3
#############################################################################
# Filename    : Motor.py
# Description : Control Motor with L293D
# Author      : Rosario Paolella
# modification: 2021/02/10
########################################################################
#import RPi.GPIO as GPIO
#from ADCDevice import *
#from gpiozero import Motor
from PIL import Image, ImageTk
from guizero import *
import time

#Class Defintions #####################################################
class MotorHelix:

    __directions=["Stop","forward","backward"]
    __helixPicture=None
    __angle=0
    __img_Left=0
    __img_Top=0
    __img_Width=100
    __img_Height=100
    
    dutycycle=0   #duty cycle of the motor
    adcValue=0    #adcValue read from potentiometer
    canvas=None
    direction=__directions[1]
    canvasWidth=0
    canvasHeight=0

        
    def __init__(self, canvas,picture):
        self.__helixPicture=picture
        self.__angle=0
        self.dutycycle = 0
        self.adcValue=0
        self.direction=self.__directions[0]
        self.canvas=canvas
        self.canvasWidth=0
        self.canvasHeight=0
    
    #set image size as half of window size and center on screen
    def SetImageSize(self):
        self.__img_Width=int(self.canvasWidth/2)
        ratio=self.__img_Width/self.__helixPicture.width
        self.__img_Height=int(self.__helixPicture.width*ratio)    
        self.__img_Left=self.canvasWidth/2-self.__img_Width/2
        self.__img_Top= self.canvasHeight/2-self.__img_Height/2  

    def DrawHelix(self):
        self.canvas.clear()
        self.SetImageSize()

        ImagetoDraw=self.__helixPicture
        ImagetoDraw=ImagetoDraw.resize((self.__img_Width ,self.__img_Height), Image.ANTIALIAS)
        ImagetoDraw=ImagetoDraw.rotate(self.__angle)
        tkImage=ImageTk.PhotoImage(ImagetoDraw)
        self.canvas.image(self.__img_Left, self.__img_Top,tkImage)
        self.__angle=(self.__angle+10)%360
               
        print ("draw helix")

############functions###################################################
def on_resize(event):
    motor.canvasWidth=event.width
    motor.canvasHeight=event.height

def ProcessData():
    #print ("process data")
    motor.DrawHelix()

    txtValue.value=motor.adcValue
    txtDirection.value=motor.direction
    txtSpeed.value=motor.dutycycle

def Clean():
    print ("Clean GPIO")
    #adc.close()
    #GPIO.cleanup()

#############APPLICATION ################################################
app = App(title="Motor with L293D")
app.bg="white"

#current width and height of the color box used to draw circle in the middle
currentWidth=0
currentHeight=0

#Gui Design#################################################
title_box = Box(app, width="fill", align="top")

#######Box with Termometer Graphics
helix_box = Box(app, width="fill", height="fill" , align="top",border=True)
#use tk to add on_resize event
helix_box.tk.bind('<Configure>', on_resize) 

#Load Helix Picure
images_dir = dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\images\\"

T_Canvas = Drawing(helix_box,width="fill",height="fill")

picture = Image.open(images_dir + "helix.png")

motor=MotorHelix(T_Canvas,picture)

#####Box with Textual Info
info_box = Box(app, width="fill", align="bottom")
Text(info_box, text="Read Value (Potentiometer) :",align="left",width="fill",size=10)
txtValue= Text(info_box, text="N/A", align="left",width="fill",size=12)
Text(info_box, text="Direction :",align="left",width="fill",size=10)
txtDirection= Text(info_box, text="N/A", align="left",width="fill",size=12)
Text(info_box, text="Speed (Duty Cycle) :",align="left",width="fill",size=10)
txtSpeed= Text(info_box, text="N/A", align="left",width="fill",size=12)

app.repeat(100,ProcessData)

app.display()
app.when_closed= Clean()