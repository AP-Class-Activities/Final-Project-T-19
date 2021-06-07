import pygame
from pygame.locals import *
from pygame_functions import *
from datetime import datetime
import inspect
import string
import json
import math
import random
import time
import os
import sys


pygame.init()
W, H = 640, 384
screenSize(W,H)

setWindowTitle("Gravity Ninja")
setIcon('images/icon.png')

bg = makeSprite("images/bg.png")
showSprite(bg)
moveSprite(bg, 320, 192, True)


class player:

    def __init__(self,xpos,ypos,grav,spr):
        self.xpos = xpos
        self.ypos = ypos
        self.grav = grav
        self.sprite = makeSprite(spr)
        self.xgrav = 1
        self.inAir = False
        self.mg = "regG"
        showSprite(self.sprite)
        moveSprite(self.sprite, xpos, ypos, True)

    def move(self):
        if (keyPressed("up") and self.inAir == False and self.mg == "regG"):
            transformSprite(self.sprite, 0, 1, hflip=True, vflip=True)
            self.xgrav = -1
        elif (keyPressed("down") and self.inAir == False and self.mg == "revG"):
            transformSprite(self.sprite, 0, 1, hflip=False, vflip=False)
            self.xgrav = 1

        self.ypos += (self.grav * self.xgrav)
        moveSprite(self.sprite, self.xpos, self.ypos, True)

        if self.ypos >= 322:
            self.xgrav = 0
            self.mg = "regG"
            self.inAir = False
        elif self.ypos <= 110:
            self.xgrav = 0
            self.mg = "revG"
            self.inAir = False
        else:
            self.inAir = True


pl = player(112,322,6,"images/mainc.png")

run = True
while run:

    # if (keyPressed("left")):
    #     W , H = H , W
    #     screenSize(W,H)
    #     rotateSprite(pl, 90)
    #     rotateSprite(bg, 90)
    #     waitPress()

    pl.move()

    tick(60)


