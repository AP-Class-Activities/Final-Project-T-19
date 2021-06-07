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
W, H = 640, 384 #tool o arze windows
screenSize(W,H)

setWindowTitle("Gravity Ninja")
setIcon('images/icon.png')

bg = makeSprite("images/bg.png") #background
showSprite(bg)
moveSprite(bg, 320, 192, True) # az gooshe windows be vasat windows montaghel kardam


class player:

    def __init__(self,xpos,ypos,grav,spr):
        self.xpos = xpos
        self.ypos = ypos
        self.grav = grav #har che ghadr bishtar bashe jazebe bishtare
        self.sprite = makeSprite(spr) #akse player
        self.xgrav = 1 # age -1 beshe yani jazabe bar aks shode
        self.inAir = False #in vase ine ke vasat paridan natooni jazabe taghir bedi
        self.mg = "regG" # in nabashe player toye zamin fooroo mire
        showSprite(self.sprite)
        moveSprite(self.sprite, xpos, ypos, True) #jayegah player

    def move(self):
        if (keyPressed("up") and self.inAir == False and self.mg == "regG"):
            transformSprite(self.sprite, 0, 1, hflip=True, vflip=True) #player ro bar aks mikone
            self.xgrav = -1                                             #jazebe bar aks mishe
        elif (keyPressed("down") and self.inAir == False and self.mg == "revG"):
            transformSprite(self.sprite, 0, 1, hflip=False, vflip=False)
            self.xgrav = 1                                              #jazebe bar migarde halat addi

        self.ypos += (self.grav * self.xgrav) # mokhtasat y player ro hesab mikone
        moveSprite(self.sprite, self.xpos, self.ypos, True) #bar asas jazabe player tekoon mikhore

        if self.ypos >= 322: #in ve tor movaghat ye zamin dorost mikone ta player roosh vayste
            self.xgrav = 0 #baad ina ro be ye class "floor" ya "wall" ke ye objecte jodas montaghel mikonim
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

    # if (keyPressed("left")): #in size windows ro tagheer mide. shayad be dard bokhore baadan.
    #     W , H = H , W
    #     screenSize(W,H)
    #     rotateSprite(pl, 90)
    #     rotateSprite(bg, 90)
    #     waitPress()

    pl.move()

    tick(60) #fps barname


