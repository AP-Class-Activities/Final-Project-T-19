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

        if pl.alive == True:
            pl.spawn()
            spawnerC.spawnCoin()
            spawnerB.spawnBlock()
            pl.collisionCheck()
            scrollBackground(scrollSpeed, 0)  # harekate background
            spawnerE.spawnHazard(320, 96,"images/spr_enemy.png",enemylist,type= "Enemy")
            spawnerS.spawnHazard(346, 69, "images/spr_spike.png", spikelist,type= "Spike")


        if pl.ypos > 450 or pl.ypos < -32: #fall damage
            pl.despawn()

        if clock() > targetTime:
            targetTime = clock() + 1000 #points per second
            scoreboard.Addscore(1)

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




        if (keyPressed("k")) and pl.alive == False: #kelid k = koshtan player
            pl.despawn()


        if (keyPressed("s")):
            scoreboard.Addscore(1)



        tick(60) #fps

        updateDisplay() #update


