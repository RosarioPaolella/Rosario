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


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,size):
        super(SpaceShip, self).__init__()
       
        self.surf=pygame.image.load(images_dir + "space_ship.png")
        self.surf=pygame.transform.scale(self.surf,(76,76) )
        self.rect = self.surf.get_rect()
        self.window_Size=size


    #attributes for movement and rotation
    velocity=1
    speed = [0, 0]
        
        
def ProcessEvents(objToMove):
    global screen
    #rotate sample
    #ball=pygame.transform.rotate(ball, 90)
   # ballrect = ball.get_rect()

    FPS=300
    cl=pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

            elif event.type==pygame.VIDEORESIZE:
                objToMove.window_Size=event.size
                pygame.display.set_mode(event.size,pygame.RESIZABLE)
            elif event.type==pygame.KEYDOWN:
                if(event.key==pygame.K_LEFT ):
                    objToMove.speed[0]=-velocity
                elif (event.key==pygame.K_RIGHT ):
                    objToMove.speed[0]=velocity
                elif (event.key==pygame.K_UP ):
                    objToMove.speed[1]=-velocity
                elif (event.key==pygame.K_DOWN ):
                    objToMove.speed[1]=velocity
            elif event.type==pygame.KEYUP :
                if (event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT):
                    objToMove.speed[0]=0
                elif (event.key==pygame.K_UP or event.key==pygame.K_DOWN):
                    objToMove.speed[1]=0

        #manage margins  
        if objToMove.rect.left < 0:
             objToMove.rect.left =0
        if objToMove.rect.right > objToMove.window_Size[0]: 
            objToMove.rect.right =objToMove.window_Size[0]

        if objToMove.rect.top < 0 :
            objToMove.rect.top =0
        if objToMove.rect.bottom > objToMove.window_Size[1]:
            objToMove.rect.bottom = objToMove.window_Size[1]

       
        objToMove.rect=objToMove.rect.move(objToMove.speed)

        #draw background 
        screen.fill((0,0,0))
        screen.blit(bg,(0,0))

        #draw in the new position
        screen.blit(objToMove.surf, objToMove.rect)

        pygame.display.flip()
        cl.tick(FPS)    



#set imageS dir
images_dir = dir_path = os.path.dirname(os.path.realpath(__file__)) + "/images/"

pygame.init()
size = width, height = 500, 500
velocity=1
speed = [0, 0]


screen = pygame.display.set_mode(size,pygame.RESIZABLE)
pygame.display.set_caption("GPIO Joystick Sample")

bg = pygame.image.load(images_dir + "space_bg.jpg")
ship=SpaceShip(size)

while True: 
    ProcessEvents(ship)

