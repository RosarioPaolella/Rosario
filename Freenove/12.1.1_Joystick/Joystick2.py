#!/usr/bin/env python3
#############################################################################
# Filename    : Joystick.py
# Description : Read Joystick state and move a game sprite
# Author      : Rosario Paolella
# modification: 2021/02/08
########################################################################
import sys, pygame
import time
import os
import math
import RPi.GPIO as GPIO
from ADCDevice import *


########################start classes############################# 
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,size):
        super(SpaceShip, self).__init__()
               
        self.image=pygame.image.load(images_dir + "space_ship.png")
        self.image=pygame.transform.scale(self.image,(76,76) )
        self.image_orig=self.image
        self.rect = self.image.get_rect()
        self.window_Size=size
        self.angle=0
        self.angleIncrement=0
       
    #attributes for movement and rotation
    velocity=1
    velocity_keyboard=1
    speed = [0, 0]
    angle=0
    KeyboardMove=False
        
    def update(self):
        self.rotate()
        self.rect=self.rect.move(self.speed)
      
    def draw(self, surface):
        surface.blit(self.image,  self.rect)
        
    def rotate(self):
        oldCenter=self.rect.center
        self.angle=(self.angle+self.angleIncrement) %360
        self.angleIncrement=0
        
        self.image =  pygame.transform.rotate(self.image_orig, self.angle)
        self.rect= self.image.get_rect()
        self.rect.center=oldCenter
######################## end classes############################# 


########################start functions#############################         
def setup(Z_Pin):
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
    GPIO.setmode(GPIO.BOARD)        
    GPIO.setup(Z_Pin,GPIO.IN,GPIO.PUD_UP)   # set Z_Pin to pull-up mode

def GetVelocity(value):
   #Values read from ACDC device is between 0,255
   # define 4 velocity of 64 values
   if value>=120 and value<=136 : 
       return 0      #no movement  
   elif value >=80 and value<120 : 
       return -1    #left or top speed 1
   elif value >=40 and value<80 : 
       return  -2   #left or top speed 2         
   elif value >=0 and value<40 : 
       return   -3  #left or top speed 3
   elif value >=136 and value<176 : 
       return  1    #left or top speed 1
   elif value >=176 and value<216 : 
       return   2   #left or top speed 2         
   elif value >=216 and value<256 : 
       return   3  #left or top speed 3

def GetRotationAngle(V_x,V_y):
    new_angle=0
    if (V_x!=0):
        new_angle=math.atan(V_y/V_x)
        new_angle=(new_angle*180)/3.14
    return new_angle

def ProcessEvents(objToMove,Pin_Axis_Z):
    FPS=300
    cl=pygame.time.Clock()

    #process pygame events 
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                adc.close()
                GPIO.cleanup()
                sys.exit()

            elif event.type==pygame.VIDEORESIZE:
                objToMove.window_Size=event.size
                pygame.display.set_mode(event.size,pygame.RESIZABLE)

            #movement with keyboard             
            elif event.type==pygame.KEYDOWN:
                objToMove.KeyboardMove=True
                if(event.key==pygame.K_LEFT ):
                    objToMove.speed[0]=-objToMove.velocity_keyboard
                elif (event.key==pygame.K_RIGHT ):
                    objToMove.speed[0]=objToMove.velocity_keyboard
                elif (event.key==pygame.K_UP ):
                    objToMove.speed[1]=-objToMove.velocity_keyboard
                elif (event.key==pygame.K_DOWN ):
                    objToMove.speed[1]=objToMove.velocity_keyboard
                elif (event.key==pygame.K_r):
                     objToMove.angleIncrement=45
            elif event.type==pygame.KEYUP :
                objToMove.KeyboardMove=False
                if (event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT):
                    objToMove.speed[0]=0
                elif (event.key==pygame.K_UP or event.key==pygame.K_DOWN):
                    objToMove.speed[1]=0
                elif (event.key==pygame.K_r):
                    objToMove.angleIncrement=0

        #read Joystick values from ACDC (Axis X=Channel 0 , Axis Y=Channel 1) 
        val_Z = GPIO.input(Pin_Axis_Z)  #read digital value of axis Z
        val_Y = adc.analogRead(0)       # read analog value of axis X 
        val_X = adc.analogRead(1)       # read analog value of axis Y    
        

        #get Velocity Axis X and Velocity Axis Y
        velocity_X=GetVelocity(val_X)
        velocity_Y=GetVelocity(val_Y)
        rotationAngle=GetRotationAngle(velocity_X,velocity_Y)
        
        #Set Velocity if not move from keyboard
        if (not objToMove.KeyboardMove):
            objToMove.speed[0]=velocity_X
            objToMove.speed[1]=velocity_Y
            objToMove.angle=rotationAngle
           
        print ('Velocity X: %d ,\tVelocity Y: %d ,\tAngle: %d ,\tAngle Inc %d'%( objToMove.speed[0], objToMove.speed[1],objToMove.angle,objToMove.angleIncrement))

        #manage margins  
        if objToMove.rect.left < 0:
             objToMove.rect.left =0
        if objToMove.rect.right > objToMove.window_Size[0]: 
            objToMove.rect.right =objToMove.window_Size[0]

        if objToMove.rect.top < 0 :
            objToMove.rect.top =0
        if objToMove.rect.bottom > objToMove.window_Size[1]:
            objToMove.rect.bottom = objToMove.window_Size[1]

        #draw background 
        screen.blit(bg,(0,0))

        #draw in the new position
        objToMove.update()
        objToMove.draw(screen)

        pygame.display.flip()
        cl.tick(FPS)    
########################end functions############################# 


########################START APP############################# 
Z_Pin=12
adc = ADCDevice() # Define an ADCDevice class object
setup(Z_Pin) #Setup ADCD Device and Set Z_PIN on GPIO18 

#set images dir
images_dir = dir_path = os.path.dirname(os.path.realpath(__file__)) + "/images/"

pygame.init()
size = width, height = 500, 500

screen = pygame.display.set_mode(size,pygame.RESIZABLE)
pygame.display.set_caption("GPIO Joystick Sample")

bg = pygame.image.load(images_dir + "space_bg.jpg")
ship=SpaceShip(size)

ProcessEvents(ship,Z_Pin)