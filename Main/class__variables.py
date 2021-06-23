import pygame
from pygame.locals import *
from pygame_functions import *
from datetime import datetime
import json
import math
import random

pygame.init()

setAutoUpdate(False)

W, H = 640, 416 #tool o arze windows
win = screenSize(W,H)

global scrollSpeed
scrollSpeed = -7 #sorat harekate background
setBackgroundImage("images/temp_bg.png")

setWindowTitle("Gravity Ninja")
setIcon('images/icon.png')

targetTime = 0

# test sound, music and gameover text
gameover = makeLabel("GAME OVER",40,200,192,"red")
s_jump = makeSound('sounds/snd_jump.wav')
s_coin = makeSound('sounds/snd_coin.wav')
mus_test1 = makeSound('sounds/mus_inGame.wav')
mus_test2 = makeSound('sounds/mus_inMenu.wav')
#########################################

#Classes

class Spawner:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.localClock = clock()
        self.init = True
        self.P1 = 0
        self.P2 = 0
        self.PP1 = 0
        self.PP2 = 0
        self.PPP1 = 0
        self.PPP2 = 0
    def spawnCoin(self):
        global coinlist , Spr , Pt
        Spr = "images/spr_coin1.png"
        Pt = 5
        RanY = [290,240,190,140,90]
        SprList = ["images/spr_coin1.png" , "images/spr_coin2.png" , "images/spr_coin3.png" , "images/spr_coin4.png"]
        Cchance = random.randrange(1,100)
        RanTimer = random.randrange(500,1000)
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
            self.localClock = clock() + RanTimer
            coinlist.append(Coin(self.x, random.choice(RanY),11,11, Spr, Pt))
        for c in coinlist:
            c.spawn()
            if c.xpos < 0:
                coinlist.pop(coinlist.index(c))
                killSprite(c.sprite)
            if c.collide(pl.hitbox):
                coinlist.pop(coinlist.index(c))
                killSprite(c.sprite)
                c.collected = True
                playSound(s_coin)
                scoreboard.Addscore(c.point)



    def spawnHazard(self,ranY1,ranY2,spr,list,type = "Enemy"):
        global h
        RanY = [ranY1,ranY2]
        RanTimer = random.randrange(7000, 10000) #later should be affected by screen/scroll speed(which increases overtime)

        if clock() > self.localClock:
            self.localClock = clock() + RanTimer
            if type == "Enemy":
                list.append(Enemy(self.x, random.choice(RanY), 113, 58, spr , 6))
            if type == "Spike":
                list.append(Spikes(self.x, random.choice(RanY), 31, 13, spr, 4))
        for h in list:
            h.spawn()
            h.hitcheck()
            if h.HIT:
                list.pop(list.index(h))
                print("a hazard smashed player")
                pl.despawn()


    def spawnBlock(self):
        global BLOCKlist

        Bchance = random.randrange(1, 1000)
        B2chance = random.randrange(1, 1000)
        B21chance = random.randrange(1, 1000)
        B22chance = random.randrange(1, 1000)
        if clock() > self.localClock:
            self.localClock = clock() + 120
            if self.init:
                for i in range(0, 768, 32):
                    BLOCKlist.append(Block(0 + i, 18, 32, 32, "images/spr_block.png"))
                    BLOCKlist.append(Block(0 + i, 50, 32, 32, "images/spr_block.png"))
                    BLOCKlist.append(Block(0 + i, 400, 32, 32, "images/spr_block.png"))
                    BLOCKlist.append(Block(0 + i, 368, 32, 32, "images/spr_block.png"))
                self.init = False




            if (1 < Bchance < 850 and self.P1 == 4) or self.P1 == 0:
                self.P1 = 4
                BLOCKlist.append(Block(640, 18, 32, 32, "images/spr_block.png"))
                BLOCKlist.append(Block(640, 50, 32, 32, "images/spr_block.png"))
                if self.PP1 > 1:
                    BLOCKlist.append(Block(640, 82, 32, 32, "images/spr_block.png"))

                    if self.PPP1 > 1:
                        BLOCKlist.append(Block(640, 114, 32, 32, "images/spr_block.png"))
            else:
                self.P1 -= 1


            if (1 < B2chance < 850 and self.P2 == 4) or self.P2 == 0 or self.PP2 > 0:
                self.P2 = 4
                BLOCKlist.append(Block(640, 400, 32, 32, "images/spr_block.png"))
                BLOCKlist.append(Block(640, 368, 32, 32, "images/spr_block.png"))
                if self.PP2 > 1:
                    BLOCKlist.append(Block(640, 336, 32, 32, "images/spr_block.png"))

                    if self.PPP2 > 1:
                        BLOCKlist.append(Block(640, 304, 32, 32, "images/spr_block.png"))
            else:
                self.P2 -= 1
                self.PP2 = 0


            if B21chance > 500:
                self.PP1 += 1

                if self.PP1 > 4:
                    self.PP1 = -2

                if B22chance > 400 and self.PP2 == 1:
                    self.PPP1 += 1

                    if self.PPP1 > 4:
                        self.PPP1 = -2


            if B22chance > 500:
                self.PP2 += 1

                if self.PP2 > 4:
                    self.PP2 = -2

                if B21chance > 400 and self.PP2 == 1:
                    self.PPP2 += 1

                    if self.PPP2 > 4:
                        self.PPP2 = -2




        for b in BLOCKlist:
            b.spawn()
            if b.xpos < -100:
                BLOCKlist.pop(BLOCKlist.index(b))
                killSprite(b.sprite)


class Player:

    def __init__(self,xpos,ypos,width,height,spr):
        self.alive = True
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.grav = 5.5 #har che ghadr bishtar bashe jazebe bishtare
        self.sprite = makeSprite(spr,frames=32) #akse player
        self.xgrav = 1 # age -1 beshe yani jazabe bar aks shode
        self.inAir = True #in vase ine ke vasat paridan natooni jazabe taghir bedi
        self.mg = 0 # main gravity ---> 0 main gravity , 1 reverse gravity
        self.pl_death_spr = makeSprite("images/spr_pldeath.png",frames=2)
        ##### marboot be animation va hitbox
        self.frame = 0
        self.gframe = 8
        self.localClock = clock()
        self.hitbox = (self.xpos - 15, self.ypos - 25, self.width - 8, self.height)

    def spawn(self):

        if self.alive:  # check mikone ke player zende hast ya na
            showSprite(self.sprite)
            if clock() > self.localClock:  ##### marboot be animation
                self.frame = (self.frame+1)%self.gframe
                self.localClock += 60

            #control player

            if (keyPressed("up") and self.inAir == False and self.mg == 0 and self.xgrav == 0): #kelid bala ro bezanin player mipare bala. hamchenin check mikone ke 1.player toye hava nist 2.player roye zamine (2 baad taghir mikone)
                playSound(s_jump)
                self.inAir = True
                self.mg = 1
                self.xgrav = -1
            elif (keyPressed("down") and self.inAir == False and self.mg == 1 and self.xgrav == 0): #mesle ghabli vali baraye az bala be paeen omadane player (kelid paeen ro bezanim mipare paeen)
                playSound(s_jump)
                self.inAir = True
                self.mg = 0
                self.xgrav = 1

            self.ypos += (self.grav * self.xgrav) # mokhtasat y player ro hesab mikone
            moveSprite(self.sprite, self.xpos, self.ypos, True) #bar asas jazabe player tekoon mikhore

            #Animatione player
            if self.inAir == False:
                self.gframe = 4
                if self.mg == 0 :
                    changeSpriteImage(self.sprite, 0 * 8 + self.frame)
                elif self.mg == 1 :
                    changeSpriteImage(self.sprite, 1 * 8 + self.frame)
            elif self.inAir == True:
                self.gframe = 4
                if self.mg == 0 :
                    #changeSpriteImage(self.sprite, 4 * 4 + self.frame)
                    changeSpriteImage(self.sprite, 21)
                elif self.mg == 1:
                    #changeSpriteImage(self.sprite, 6 * 4 + self.frame)
                    changeSpriteImage(self.sprite, 27)


            self.hitbox = (self.xpos - 15, self.ypos - 25, self.width - 8, self.height)
        #pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)

    def collide(self, rect):
        if self.alive:
            if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                    return True
        return False

    def collisionCheck(self):
        if self.alive:
            if self.mg == 0:
                self.xgrav = 1
            if self.mg == 1:
                self.xgrav = -1


            global i
            for i in BLOCKlist:

                if i.collide(i.pitbox,self.hitbox):
                    self.inAir = False
                    self.xgrav = 0

                if i.collide(i.hitbox,self.hitbox):
                    self.despawn()
                    print("player hit a block")

    def despawn(self): #player mimire va spritesh az bane mire
        if self.alive == True:
            self.alive = False
            killSprite(self.sprite)
            showSprite(self.pl_death_spr)
            moveSprite(self.pl_death_spr, self.xpos, self.ypos, True)
            changeSpriteImage(self.pl_death_spr,self.mg)
            print("Player is dead")
            showLabel(gameover)
            # test music(music momkene ziad boland bashe, check konin)
            stopSound(mus_test1)
            playSound(mus_test2, loops=-1)  # loop = -1 bashe bi nahyat loop mishe



class Coin:
    def __init__(self,xpos,ypos,width,height,spr,point):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr,frames= 8)
        self.speed = 4
        self.point = point
        self.collected = False
        self.frame = 0
        self.gframe = 8
        self.localClock = clock()
    def spawn(self):

        if self.collected == False:
            if clock() > self.localClock:
                self.frame = (self.frame + 1) % self.gframe
                self.localClock += 60

            showSprite(self.sprite)
            self.xpos -= self.speed
            moveSprite(self.sprite, self.xpos, self.ypos, True)
            changeSpriteImage(self.sprite, 0 * 8 + self.frame)

        self.hitbox = (self.xpos - 5.5, self.ypos - 5.5, self.width, self.height)

        global z
        for z in BLOCKlist:
            if z.collide(z.pitbox,self.hitbox):
                killSprite(self.sprite)
                self.x = -999
        # pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

class Enemy:
    def __init__(self, xpos, ypos, width, height, spr , speed):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr,frames=2)
        self.speed = speed
        self.HIT = False

        self.hitbox = (self.xpos - 46.5, self.ypos - 29, self.width - 36, self.height)

    def spawn(self):
        showSprite(self.sprite)
        self.xpos -= self.speed
        if self.ypos <= 96:
            changeSpriteImage(self.sprite,1)
        else:
            changeSpriteImage(self.sprite,0)

        moveSprite(self.sprite, self.xpos, self.ypos, True)



        if self.xpos < -50:
            killSprite(self.sprite)

        if pl.collide(self.hitbox):
            self.HIT = True

    def hitcheck(self):
        self.hitbox = (self.xpos - 46.5, self.ypos - 29, self.width - 36, self.height)
        # pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False


class Spikes(Enemy):
    def __init__(self, xpos, ypos, width, height, spr, speed):
        super().__init__(xpos, ypos, width, height, spr, speed)
        self.HIT = False


    def hitcheck(self):
        self.hitbox = (self.xpos - 15.5, self.ypos - 6.5, self.width, self.height)
        self.citbox = (self.xpos - 15.5, self.ypos - 32, self.width, self.height + 32) #to prevent midair spikes(not working yet)

        #pygame.draw.rect(win, (0, 0, 255), self.citbox, 2)

    def collide(self, hit, rect):
        if rect[0] + rect[2] > hit[0] and rect[0] < hit[0] + hit[2]:
            if rect[1] + rect[3] > hit[1] and rect[1] < hit[1] + hit[3]:
                return True
        return False


class Block:
    def __init__(self,xpos,ypos,width,height,spr):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr)
        self.speed = 4
        self.frame = 0
        self.gframe = 8
        self.localClock = clock()
        self.hitbox = (self.xpos - 16, self.ypos - 16, self.width, self.height)
        self.pitbox = (self.xpos - 19, self.ypos - 22, self.width + 4, self.height + 8)
    def spawn(self):
        showSprite(self.sprite)
        self.xpos -= self.speed
        moveSprite(self.sprite, self.xpos, self.ypos, True)

        self.hitbox = (self.xpos - 16, self.ypos - 16, self.width, self.height)
        self.pitbox = (self.xpos - 19, self.ypos - 22, self.width + 4, self.height + 14)
        #pygame.draw.rect(win, (0, 0, 255), self.pitbox, 2)

    def collide(self, hit,rect):
        if rect[0] + rect[2] > hit[0] and rect[0] < hit[0] + hit[2]:
            if rect[1] + rect[3] > hit[1] and rect[1] < hit[1] + hit[3]:
                return True
        return False

class ScoreSystem:
    def __init__(self, xpos, ypos,size): #sprite too?
        self.score = 0
        self.body = makeLabel(str(self.score),size, xpos, ypos, "white" , font="Fipps-Regular")
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


class MusicPlayer:
    pass




#define objects


global pl
pl = Player(200,240,45,45,"images/SPR_NINJA.png")

spawnerC = Spawner(864,322) #coin
spawnerE = Spawner(864,322) #enemy
spawnerS = Spawner(800,322) #spike
spawnerB = Spawner(800,64) #block

global scoreboard
scoreboard = ScoreSystem(575,10,40)
scoreboard.draw()

coinlist = [Coin(-999, -999,11,11, "images/spr_coin1.png", 20)]
enemylist = [Enemy(-999, -999,113,58, "images/spr_enemy.png",6)]
spikelist =[Spikes(-999, -999,113,58, "images/spr_enemy.png",6)]
BLOCKlist = [Block(-999, -999,113,58, "images/spr_enemy.png")]



playSound(mus_test1,loops=-1) #turn to class (music player)



