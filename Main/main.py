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

setAutoUpdate(False)

W, H = 640, 384 #tool o arze windows
win = screenSize(W,H)

scrollSpeed = -5 #sorat harekate background

setBackgroundImage("images/bg.png")

setWindowTitle("Gravity Ninja")
setIcon('images/icon.png')

#targetTime = 0

############ test sound, music and gameover text
gameover = makeLabel("GAME OVER",40,200,192,"black")
s_jump = makeSound('sounds/Jump.wav')
mus_test1 = makeSound('sounds/mus_inGame.wav')
mus_test2 = makeSound('sounds/mus_inMenu.wav')
#############


class player:

    def __init__(self,xpos,ypos,grav,spr):
        self.alive = True
        self.xpos = xpos
        self.ypos = ypos
        self.grav = grav #har che ghadr bishtar bashe jazebe bishtare
        self.sprite = makeSprite(spr,frames=32) #akse player
        self.xgrav = 1 # age -1 beshe yani jazabe bar aks shode
        self.inAir = False #in vase ine ke vasat paridan natooni jazabe taghir bedi
        self.mg = "regG" # in nabashe player toye zamin fooroo mire (zamin kononie player ro taeen mikone)
        showSprite(self.sprite)
        ##### marboot be animation
        self.frame = 0
        self.gframe = 8
        self.theTime = clock()
        #
        # self.a0 = False
        # self.a1 = False
    def START(self):

        if clock() > self.theTime:  ##### marboot be animation
            self.frame = (self.frame+1)%self.gframe
            self.theTime += 60

        if self.alive: #check mikone ke player zende hast ya na
        
            #control player
        
            if (keyPressed("up") and self.inAir == False and self.mg == "regG"): #kelid bala ro bezanin player mipare bala. hamchenin check mikone ke 1.player toye hava nist 2.player roye zamine (2 baad taghir mikone)

                playSound(s_jump)
                print("Player is alive")
                #transformSprite(self.sprite, 0, 1, hflip=True, vflip=True) #player ro bar aks mikone
                self.xgrav = -1                                             #jazebe bar aks mishe
            elif (keyPressed("down") and self.inAir == False and self.mg == "revG"): #mesle ghabli vali baraye az bala be paeen omadane player (kelid paeen ro bezanim mipare paeen)
                playSound(s_jump)
                print("Player is alive")
                #transformSprite(self.sprite, 0, 1, hflip=False, vflip=False)
                self.xgrav = 1                                              #jazebe bar migarde halat addi

            self.ypos += (self.grav * self.xgrav) # mokhtasat y player ro hesab mikone
            moveSprite(self.sprite, self.xpos, self.ypos, True) #bar asas jazabe player tekoon mikhore




            if self.ypos >= 320: #in be tor movaghat ye zamin dorost mikone ta player roosh vayste
                self.xgrav = 0 #baad ina ro be ye class "floor" ya "wall" ke ye objecte jodas montaghel mikonim
                self.mg = "regG"
                self.inAir = False

            elif self.ypos <= 64:
                self.xgrav = 0
                self.mg = "revG"
                self.inAir = False

            else:
                self.inAir = True


            #Animatione player
            if self.inAir == False:
                self.gframe = 4
                if self.mg == "regG" :
                    changeSpriteImage(self.sprite, 0 * 8 + self.frame)
                elif self.mg == "revG" :
                    changeSpriteImage(self.sprite, 1 * 8 + self.frame)
# middle 192
            elif self.inAir == True:
                self.gframe = 4
                if self.mg == "regG" :
                    #changeSpriteImage(self.sprite, 4 * 4 + self.frame)
                    changeSpriteImage(self.sprite, 21)
                elif self.mg == "revG":
                    #changeSpriteImage(self.sprite, 6 * 4 + self.frame)
                    changeSpriteImage(self.sprite, 27)

    def draw(self):
        pass

    def KILL(self): #player mimire va spritesh az bane mire
        if self.alive == True:
            self.alive = False
            print("Player is dead")
            killSprite(self.sprite)
            #test music(music momkene ziad boland bashe, check konin)
            stopSound(mus_test1)
            playSound(mus_test2, loops=-1) #loop = -1 bashe bi nahyat loop mishe

class testobj:
    def __init__(self,xpos,ypos,spr):
        self.xpos = xpos
        self.ypos = ypos
        self.sprite = makeSprite(spr)




pl = player(112,322,7,"images/SPR_NINJA.png")


playSound(mus_test1,loops=-1) #turn to class (music player)

run = True
while run:

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

    scrollBackground(scrollSpeed, 0) #harekate background
    pl.START()
    ############################

    if (keyPressed("k")): #kelid k = koshtan player
        pl.KILL()
        scrollSpeed = 1
        showLabel(gameover)


    tick(60) #fps
    updateDisplay() #update


