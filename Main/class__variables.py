import pygame
from pygame.locals import *
from pygame_functions import *
from datetime import datetime
import json
import math
import random

pygame.init()

setAutoUpdate(False)

W, H = 640, 384 #tool o arze windows
win = screenSize(W,H)

scrollSpeed = -5 #sorat harekate background
setBackgroundImage("images/bg.png")

setWindowTitle("Gravity Ninja")
setIcon('images/icon.png')

targetTime = 0

# test sound, music and gameover text
gameover = makeLabel("GAME OVER",40,200,192,"black")
s_jump = makeSound('sounds/snd_jump.wav')
s_coin = makeSound('sounds/snd_coin.wav')
mus_test1 = makeSound('sounds/mus_inGame.wav')
mus_test2 = makeSound('sounds/mus_inMenu.wav')
#########################################

#Classes

class Player:

    def __init__(self,xpos,ypos,width,height,grav,spr):
        self.alive = True
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.grav = grav #har che ghadr bishtar bashe jazebe bishtare
        self.sprite = makeSprite(spr,frames=32) #akse player
        self.xgrav = 1 # age -1 beshe yani jazabe bar aks shode
        self.inAir = False #in vase ine ke vasat paridan natooni jazabe taghir bedi
        self.mg = "regG" # in nabashe player toye zamin fooroo mire (zamin kononie player ro taeen mikone)

        ##### marboot be animation va hitbox
        self.frame = 0
        self.gframe = 8
        self.localClock = clock()
        self.hitbox = (self.xpos - 5.5, self.ypos - 5.5, self.width, self.height)

    def spawn(self):
        showSprite(self.sprite)
        if clock() > self.localClock:  ##### marboot be animation
            self.frame = (self.frame+1)%self.gframe
            self.localClock += 60

        if self.alive: #check mikone ke player zende hast ya na
        
            #control player
        
            if (keyPressed("up") and self.inAir == False and self.mg == "regG"): #kelid bala ro bezanin player mipare bala. hamchenin check mikone ke 1.player toye hava nist 2.player roye zamine (2 baad taghir mikone)
                playSound(s_jump)
                self.xgrav = -1                                             #jazebe bar aks mishe
            elif (keyPressed("down") and self.inAir == False and self.mg == "revG"): #mesle ghabli vali baraye az bala be paeen omadane player (kelid paeen ro bezanim mipare paeen)
                playSound(s_jump)
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
            elif self.inAir == True:
                self.gframe = 4
                if self.mg == "regG" :
                    #changeSpriteImage(self.sprite, 4 * 4 + self.frame)
                    changeSpriteImage(self.sprite, 21)
                elif self.mg == "revG":
                    #changeSpriteImage(self.sprite, 6 * 4 + self.frame)
                    changeSpriteImage(self.sprite, 27)


            self.hitbox = (self.xpos - 25, self.ypos - 25, self.width, self.height)
        #pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)

    def despawn(self): #player mimire va spritesh az bane mire
        if self.alive == True:
            self.alive = False
            print("Player is dead")
            killSprite(self.sprite)
            #test music(music momkene ziad boland bashe, check konin)
            stopSound(mus_test1)
            playSound(mus_test2, loops=-1) #loop = -1 bashe bi nahyat loop mishe


class Spawner:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.localClock = clock()
    def spawnPlayer(self,player):
        player.spawn()
    def spawnCoin(self):
        global coinlist , x , Spr , Pt
        Spr = "images/spr_coin1.png"
        Pt = 5
        RanY = [290,240,190,140,90]
        SprList = ["images/spr_coin1.png" , "images/spr_coin2.png" , "images/spr_coin3.png" , "images/spr_coin4.png"]
        Cchance = random.randrange(1,100)
        RanTimer = random.randrange(500,7000)
        if Cchance >= 55:
            Spr = SprList[0]
            Pt = 5
        elif 29 < Cchance < 55:
            Spr = SprList[1]
            Pt = 10
        elif 1 < Cchance < 15:
            Spr = SprList[2]
            Pt = 20
        elif Cchance == 1:
            Spr = SprList[3]
            Pt = 200

        if clock() > self.localClock:
            self.localClock = clock() + 1#RanTimer
            coinlist.append(Coin(self.x, random.choice(RanY),11,11, Spr, Pt))
        for x in coinlist:
            x.spawn()
            if x.collide(pl.hitbox):
                coinlist.pop(coinlist.index(x))
                killSprite(x.sprite)
                playSound(s_coin)
                x.collected = True
                scoreboard.Addscore(x.point)


class Coin:
    def __init__(self,xpos,ypos,width,height,spr,point):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr,frames= 8)
        self.point = point
        self.collected = False
        self.hitbox = (self.xpos, self.ypos, self.width, self.height)
        self.frame = 0
        self.gframe = 8
        self.localClock = clock()
    def spawn(self):

        if self.collected == False:
            if clock() > self.localClock:
                self.frame = (self.frame + 1) % self.gframe
                self.localClock += 60

            showSprite(self.sprite)
            self.xpos -= 2
            moveSprite(self.sprite, self.xpos, self.ypos, True)
            changeSpriteImage(self.sprite, 0 * 8 + self.frame)

        if self.xpos < 0:
            killSprite(self.sprite)
            self.collected = True

        self.hitbox = (self.xpos - 5.5, self.ypos - 5.5, self.width, self.height)
        # pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False


class ScoreSystem:
    def __init__(self, xpos, ypos,size): #sprite too?
        self.score = 0
        self.body = makeLabel(str(self.score),size, xpos, ypos, "black")
    def Reset(self):
        self.score = 0
    def Setscore(self,num):
        self.score = num
        changeLabel(self.body,str(self.score))
    def Addscore(self,num):
        self.score += num
        changeLabel(self.body, str(self.score))
    def testprint(self):
        print(self.score)
    def draw(self):
        showLabel(self.body)


class Enemy:
    def __init__(self,xpos,ypos,spr):
        self.xpos = xpos
        self.ypos = ypos
        self.sprite = makeSprite(spr)


class MusicPlayer:
    pass


#define objects


global pl
pl = Player(112,322,45,45,7,"images/SPR_NINJA.png")

spawnerP = Spawner(112,322)
spawnerC = Spawner(750,322)

global scoreboard
scoreboard = ScoreSystem(575,10,40)
scoreboard.draw()

coinlist = [Coin(-999, -999,11,11, "images/spr_coin1.png", 20)]

playSound(mus_test1,loops=-1) #turn to class (music player)

