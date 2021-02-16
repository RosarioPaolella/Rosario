#!/usr/bin/env python3
#############################################################################
# Filename    : Motor.py
# Description : Control Motor with L293D
# Author      : Rosario Paolella
# modification: 2021/02/10
########################################################################
#import RPi.GPIO as GPIO
from ADCDevice import *
from gpiozero import Motor
from PIL import Image, ImageTk
from guizero import *
from ACDCMapper import *
import cv2
import time

#Class Defintions #####################################################
class MotorHelix:

    __directions=["Stop","Backward","Forward"]
    __helixPicture=None
    __angle=0
    __speed=0
    __img_Left=0
    __img_Top=0
    __img_Width=100
    __img_Height=100
    
    adcValue=128    #adcValue read from potentiometer
    canvas=None
    direction=__directions[1]
    canvasWidth=0
    canvasHeight=0

        
    def __init__(self, canvas,picture):
        self.__helixPicture=picture
        self.__angle=0
        self.adcValue=255
        self.direction=self.__directions[0]
        self.canvas=canvas
        self.canvasWidth=0
        self.canvasHeight=0
        
        self.mappedValues=ADCDMapper()
        self.SetMappedValues()

    def SetMappedValues(self):
        self.mappedValues.SetMapping(0,30,-25)
        self.mappedValues.SetMapping(30,40,-22)
        self.mappedValues.SetMapping(40,50,-19)
        self.mappedValues.SetMapping(50,60,-16)
        self.mappedValues.SetMapping(60,70,-13)
        self.mappedValues.SetMapping(70,80,-10)
        self.mappedValues.SetMapping(80,90,-7)
        self.mappedValues.SetMapping(90,100,-4)
        self.mappedValues.SetMapping(100,110,-1)
        self.mappedValues.SetMapping(110,150,0)
        self.mappedValues.SetMapping(150,160,1)
        self.mappedValues.SetMapping(160,170,4)
        self.mappedValues.SetMapping(170,180,7)
        self.mappedValues.SetMapping(180,190,10)
        self.mappedValues.SetMapping(190,200,13)
        self.mappedValues.SetMapping(200,210,16)
        self.mappedValues.SetMapping(210,220,19)
        self.mappedValues.SetMapping(220,230,22)
        self.mappedValues.SetMapping(230,256,25)        


#set image size as half of window size and center on screen

    def SetImageSize(self):

        width, height =  self.__helixPicture.shape[:2]
        self.__img_Width=int(self.canvasWidth/2)
        ratio=self.__img_Width/width
        self.__img_Height=int(width*ratio)   
        self.__img_Left=self.canvasWidth/2-self.__img_Width/2
        self.__img_Top= self.canvasHeight/2-self.__img_Height/2 

 

    def rotate(self,image, angle, center = None, scale = 1.0):

        (h, w) = image.shape[:2]

        if center is None:
            center = (w / 2, h / 2)

        # Perform the rotation
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h),borderValue=(255,255,255))
        return rotated

    def DrawHelix(self):
        self.canvas.clear()
        self.SetImageSize()

        #set speed rotation based on acdcValue
        self.speed=self.mappedValues.GetMappedValue(self.adcValue)
        #set direction based on speed
        if (self.speed==0) : self.direction=self.__directions[0]
        if (self.speed>0) : self.direction=self.__directions[1]
        if (self.speed<0) : self.direction=self.__directions[2]
        
        ImagetoDraw=self.__helixPicture
        ImagetoDraw = cv2.cvtColor(ImagetoDraw, cv2.COLOR_BGR2RGB)
        ImagetoDraw= cv2.resize(ImagetoDraw, (self.__img_Width ,self.__img_Height), interpolation = cv2.INTER_AREA)
        ImagetoDraw=self.rotate(ImagetoDraw,(self.__angle))

        # convert the images to PIL format...
        ImagetoDraw = Image.fromarray(ImagetoDraw)
        tkImage = ImageTk.PhotoImage(ImagetoDraw)
        self.canvas.image(self.__img_Left, self.__img_Top,tkImage)
        
        self.__angle=(self.__angle+self.speed)%360

############functions###################################################
def on_resize(event):
    motor.canvasWidth=event.width
    motor.canvasHeight=event.height
    motor.DrawHelix()

# mapNUM function: map the value from a range of mapping to another range.
def mapNUM(value,fromLow,fromHigh,toLow,toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

def ProcessData():
    value = adc.analogRead(0) # read ADC value of channel 0

    motor.adcValue=value

    #move motor device 
    value = value -128
    speed=mapNUM(abs(value),0,128,0,100)
    if (speed > 0):
        motor_device.forward(speed/100)
    if (speed < 0):
        motor_device.backward(speed/100)
    if (speed == 0):
        motor_device.stop()
    #draw motor on screen 
    motor.DrawHelix()



    txtValue.value=motor.adcValue
    txtDirection.value=motor.direction
    txtSpeed.value=motor.speed


    print ('ADC Value : %d'%(value))

def Clean():
    print ("Clean GPIO")
    adc.close()
    
def setupDevices():
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
#############APPLICATION ################################################
app = App(title="Motor with L293D")
app.bg="white"

#current width and height of the color box used to draw circle in the middle
currentWidth=0
currentHeight=0

###Setup Devices
adc = ADCDevice() 

motoRPin1 = 27 #connected with pin IN1 of L293D
motoRPin2 = 17 #connected with pin IN1 of L293D
enablePin = 22 #connected with pin ENABLE1 of L293D

motor_device = Motor(motoRPin1, motoRPin2,enablePin)

setupDevices()

#Gui Design#################################################
title_box = Box(app, width="fill", align="top")

#######Box with Termometer Graphics
helix_box = Box(app, width="fill", height="fill" , align="top",border=True)
#use tk to add on_resize event
helix_box.tk.bind('<Configure>', on_resize) 

#Load Helix Picure
images_dir = dir_path = os.path.dirname(os.path.realpath(__file__)) + "/images/"

T_Canvas = Drawing(helix_box,width="fill",height="fill")

picture = cv2.imread(images_dir + "helix.png")

motor=MotorHelix(T_Canvas,picture)

#####Box with Textual Info
info_box = Box(app, width="fill", align="bottom")
Text(info_box, text="Read Value (Potentiometer) :",align="left",width="fill",size=10,font="Segoe UI")
txtValue= Text(info_box, text="N/A", align="left",width="fill",size=12,font="Segoe UI Black")
Text(info_box, text="Direction :",align="left",width="fill",size=10,font="Segoe UI")
txtDirection= Text(info_box, text="N/A", align="left",width="fill",size=12,font="Segoe UI Black")
Text(info_box, text="Speed :",align="left",width="fill",size=10,font="Segoe UI")
txtSpeed= Text(info_box, text="N/A", align="left",width="fill",size=12,font="Segoe UI Black")

app.repeat(180,ProcessData)

app.display()
app.when_closed= Clean()