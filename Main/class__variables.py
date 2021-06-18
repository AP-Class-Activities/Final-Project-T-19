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

scrollSpeed = -5 #sorat harekate background
setBackgroundImage("images/temp_bg.png")

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

class Spawner:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.localClock = clock()
        self.init = True
    def spawnCoin(self):
        global coinlist , Spr , Pt
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



    def spawnHazard(self):
        global enemylist, h
        RanY = [320, 96]
        RanTimer = random.randrange(7000, 10000) #later should be affected by screen/scroll speed(which increases overtime)

        if clock() > self.localClock:
            self.localClock = clock() + RanTimer
            enemylist.append(Enemy(self.x, random.choice(RanY), 113, 58, "images/spr_enemy.png"))
        for h in enemylist:
            h.spawn()
            if h.collide(pl.hitbox):
                enemylist.pop(enemylist.index(h))
                killSprite(h.sprite)
                pl.despawn()


    def spawnBlock(self):
        global BLOCKlist
        if clock() > self.localClock:
            self.localClock = clock() + 250
            if self.init:
                for i in range(1, 742, 32):
                    BLOCKlist.append(Block(0 + i, 18, 32, 32, "images/spr_block.png"))
                    BLOCKlist.append(Block(0 + i, 50, 32, 32, "images/spr_block.png"))
                    BLOCKlist.append(Block(0 + i, 400, 32, 32, "images/spr_block.png"))
                    BLOCKlist.append(Block(0 + i, 368, 32, 32, "images/spr_block.png"))
                self.init = False
            BLOCKlist.append(Block(640, 18, 32, 32, "images/spr_block.png"))
            BLOCKlist.append(Block(640, 50, 32, 32, "images/spr_block.png"))
            BLOCKlist.append(Block(640, 400, 32, 32, "images/spr_block.png"))
            BLOCKlist.append(Block(640, 368, 32, 32, "images/spr_block.png"))
        for b in BLOCKlist:
            b.spawn()
            if b.xpos < 0:
                BLOCKlist.pop(BLOCKlist.index(b))
                killSprite(b.sprite)


class Player:

    def __init__(self,xpos,ypos,width,height,spr):
        self.alive = True
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.grav = 7 #har che ghadr bishtar bashe jazebe bishtare
        self.sprite = makeSprite(spr,frames=32) #akse player
        self.xgrav = 1 # age -1 beshe yani jazabe bar aks shode
        self.inAir = True #in vase ine ke vasat paridan natooni jazabe taghir bedi
        self.mg = "regG" # in nabashe player toye zamin fooroo mire (zamin kononie player ro taeen mikone)
        self.Grounded = False
        self.IsonGround = False

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
        
            if (keyPressed("up") and self.inAir == False and self.Grounded == True and self.mg == "regG"): #kelid bala ro bezanin player mipare bala. hamchenin check mikone ke 1.player toye hava nist 2.player roye zamine (2 baad taghir mikone)
                playSound(s_jump)
                self.Grounded = False
                self.inAir = True
                self.mg = "revG"
                self.xgrav = -1
            elif (keyPressed("down") and self.inAir == False and self.Grounded == True and self.mg == "revG"): #mesle ghabli vali baraye az bala be paeen omadane player (kelid paeen ro bezanim mipare paeen)
                playSound(s_jump)
                self.Grounded = False
                self.inAir = True
                self.mg = "regG"
                self.xgrav = 1

            self.ypos += (self.grav * self.xgrav) # mokhtasat y player ro hesab mikone
            moveSprite(self.sprite, self.xpos, self.ypos, True) #bar asas jazabe player tekoon mikhore

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

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def collisionCheck(self):

        if self.mg == "regG":
            self.xgrav = 1
        if self.mg == "revG":
            self.xgrav = -1


        global i
        for i in BLOCKlist:

            if i.pseudoCollide(self.hitbox):
                self.Grounded = True
                self.inAir = False
                self.xgrav = 0

            if i.collide(self.hitbox):
                print("player hit a block")

    def despawn(self): #player mimire va spritesh az bane mire
        if self.alive == True:
            self.alive = False
            print("Player is dead")
            killSprite(self.sprite)
            showLabel(gameover)
            #test music(music momkene ziad boland bashe, check konin)
            stopSound(mus_test1)
            playSound(mus_test2, loops=-1) #loop = -1 bashe bi nahyat loop mishe


class Coin:
    def __init__(self,xpos,ypos,width,height,spr,point):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr,frames= 8)
        self.speed = 2
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
        # pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

class Enemy:
    def __init__(self, xpos, ypos, width, height, spr):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr,frames=2)
        self.speed = 3
        self.point = 0


    def spawn(self):
        showSprite(self.sprite)
        self.xpos -= self.speed
        if self.ypos == 96:
            changeSpriteImage(self.sprite,1)
        else:
            changeSpriteImage(self.sprite,0)

        moveSprite(self.sprite, self.xpos, self.ypos, True)

        self.hitbox = (self.xpos - 46.5, self.ypos - 29, self.width - 36, self.height)
        #pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)
        if self.xpos < -50:
            killSprite(self.sprite)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False


class Block:
    def __init__(self,xpos,ypos,width,height,spr):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.sprite = makeSprite(spr)
        self.speed = 2
        self.frame = 0
        self.gframe = 8
        self.localClock = clock()
        self.hitbox = (self.xpos - 16, self.ypos - 16, self.width, self.height)
        self.pitbox = (self.xpos - 19, self.ypos - 24, self.width + 4, self.height + 10)
    def spawn(self):
        showSprite(self.sprite)
        self.xpos -= self.speed
        moveSprite(self.sprite, self.xpos, self.ypos, True)

        self.hitbox = (self.xpos - 16, self.ypos - 16, self.width, self.height)
        self.pitbox = (self.xpos - 19, self.ypos - 20, self.width + 4, self.height + 10)
        #pygame.draw.rect(win, (0, 0, 255), self.pitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

    def pseudoCollide(self, rect):
        if rect[0] + rect[2] > self.pitbox[0] and rect[0] < self.pitbox[0] + self.pitbox[2]:
            if rect[1] + rect[3] > self.pitbox[1] and rect[1] < self.pitbox[1] + self.pitbox[3]:
                return True
        return False

class ScoreSystem:
    def __init__(self, xpos, ypos,size): #sprite too?
        self.score = 0
        self.body = makeLabel(str(self.score),size, xpos, ypos, "white")
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

spawnerC = Spawner(750,322)
spawnerH = Spawner(750,322)
spawnerB = Spawner(750,64)

global scoreboard
scoreboard = ScoreSystem(575,10,40)
scoreboard.draw()

coinlist = [Coin(-999, -999,11,11, "images/spr_coin1.png", 20)]
enemylist = [Enemy(-999, -999,113,58, "images/spr_enemy.png")]
BLOCKlist = [Block(-999, -999,113,58, "images/spr_enemy.png")]



playSound(mus_test1,loops=-1) #turn to class (music player)



