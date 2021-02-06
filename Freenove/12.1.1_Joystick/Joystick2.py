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

#set imageS dir
images_dir = dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\images\\"

pygame.init()

size = width, height = 300, 300
velocity=1
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size,pygame.RESIZABLE  )
pygame.display.set_caption("GPIO Joystick Sample")

ball = pygame.image.load(images_dir + "intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type==pygame.VIDEORESIZE:
            width=event.w
            height=event.h
        elif event.type==pygame.KEYDOWN:
            if(event.key==pygame.K_LEFT ):
                speed[0]=-velocity
            elif (event.key==pygame.K_RIGHT ):
                speed[0]=velocity
            elif (event.key==pygame.K_UP ):
                speed[1]=-velocity
            elif (event.key==pygame.K_DOWN ):
                speed[1]=velocity
        elif event.type==pygame.KEYUP :
            if (event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT):
                speed[0]=0
            elif (event.key==pygame.K_UP or event.key==pygame.K_DOWN):
                 speed[1]=0


    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    time.sleep(0.01)

    #draw in the new position
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    