#test
#class haye tarif shode dar inja faghat baraye test hast va 100% taghir mikonan

class player :
    def __init__(self,hp,x,y):
        self.x = x
        self.y = y
        self.hp = hp


    def moveto(self,x,y): # jayegahe player ro taghir mide va makane jadid ro namayesh mide
        self.x = x
        self.y = y
        print(f"player moved to ({self.x},{self.y})")


    def healthcheck(self):
        if self.hp <= 0:
            print("player is dead")
        else:
            print("player is alive")


    def displayhp(self):
        print(f"hp = {self.hp}")


    def displaycoord(self): # makane player ro be soorate (x,y) namayesh mide
        print(f'player is at ({self.x},{self.y})')


class enemy :
    def __init__(self,x,y):
        self.x = x
        self.y = y


    def moveto(self,x,y): # jayegahe enemy ro taghir mide va makane jadid ro namayesh mide
        self.x = x
        self.y = y
        print(f"enemy moved to ({self.x},{self.y})")


    def dmg (self,pl,power): #playere morede nazar va meghdar damage ro migire
        if self.x == pl.x or self.y == pl.x: #age makane enemy o player yeki bashan (be ham barkhord konan)
            pl.hp -= power
            print("damage dealt") #damage
        else: #barkhordi ijad nashod
            print("enemy missed") # no damage



    def displaycoord(self): # makane enemy ro be soorate (x,y) namayesh mide
        print(f'enemy is at ({self.x},{self.y})')


def start():
    # player va enemy sakhte shodan
    p = player(5, 32, 32)
    e = enemy(64, 64)

    # makan har do namayesh dade shod
    p.displaycoord()
    e.displaycoord()

    # enemy hamle kard
    e.dmg(p, 2)

    # vaziat player check shod
    p.healthcheck()
    p.displayhp()

    # player harekat kard va makan jadid namayesh dade shod
    p.moveto(64, 64)
    p.displaycoord()

    e.dmg(p, 2)
    p.healthcheck()
    p.displayhp()

    e.dmg(p, 222)

    p.healthcheck()
    p.displayhp()


start()


