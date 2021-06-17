import pygame
from pygame.locals import *
from class__variables import *
from pygame_functions import *
from datetime import datetime
import json
import math
import random

run = True

while run:

    pl.spawn()
    spawnerC.spawnCoin()
    spawnerH.spawnHazard()
    scrollBackground(scrollSpeed, 0)  # harekate background

    # if (keyPressed("left")): #in size windows ro tagheer mide. shayad be dard bokhore baadan.
    #     W , H = H , W
    #     screenSize(W,H)
    #     rotateSprite(pl, 90)
    #     rotateSprite(bg, 90)
    #     waitPress()

    #

    # if theTime > targetTime: #in ye timer hast vase baad
    #     targetTime = theTime + 1
    #     bgs += 10
    # if bgs == 1280:
    #     bgs = 0


    # if clock() > targetTime:
    #     targetTime = clock() + 2000
    #     scoreboard.Addscore(1)

    if (keyPressed("k")): #kelid k = koshtan player
        pl.despawn()


    if (keyPressed("s")):
        scoreboard.Addscore(1)

    tick(60) #fps

    updateDisplay() #update


