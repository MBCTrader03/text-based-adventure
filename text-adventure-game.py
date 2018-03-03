import time, random

##Super-class for all animate objects
class Animate:

    ##Constructor for Animate, sets inherited properties of the method
    def __init__(self, name, currentRoom, hitPoints, weapon, armour):
        self.name = name
        self.currentRoom = currentRoom
        self.hitPoints = hitPoints
        self.weapon = weapon
        self.armour = armour
        self.armourProtection = self.getArmourProtection(armour)
        self.dead = False
        self.attacking = False
        self.defending = False

    ##All Animate objects have a way of attacking
    def attack(self):
        print("Attack")
        self.attacking = True
        self.defending = False
        self.target.takeDamage(random.randint(self.weapon.getDamage()-2, self.weapon.getDamage()+2))

    ##All Animate objects have a way of defending
    def defend(self):
        print("Defend")
        self.defending = True
        self.attacking = True

    ##All Animate objects have a way of running
    def run(self):
        print("Attack")
        luck = random.randing(1, 100)
        if luck % 2 == 0:
            print("You escaped successfully!")
            self.defending = False
            self.attacking = False
        else: print("Your escape attempt failed")

    def takeDamage(self, damagePoints):
        print("Taking damage in super")
        ##damage taken is equal to damage given multiplied by (1 - your armour as a percentage of the maximum armour value (200)) and if defending that damage is divided by 2, 3 or 4
        if self.isDefending():
            self.hitPoints -= int((damagePoints * (1 - (self.armourProtection / 200))) / random.randint(2, 4))
        else: self.hitPoints -= int(damagePoints * (1 - (self.armourProtection / 200)))
        if self.hitPoints <= 0:
            self.die()
        print(self.hitPoints)

    def die(self):
        print(self.name + " is dead... Well done!")
        self.dead = True

    def isDead(self):
        return self.dead

    def getArmourProtection(self, armour):
        total = 0
        for piece in armour:
            total += piece.getVal()
        return total

    def decideNextMove(self):
        print("Cannae decide I'm unimplemented")

    def isDefending(self):
        return self.defending

    def isAttacking(self):
        return self.attacking

class Player(Animate):
    
    def __init__(self, name):
        super().__init__(name, 1, 100, Weapon("Hands",  5), [Armour(1, "Helmet of Beginner's Luck")])
        self.fullHitPoints = 10
    
    def getName(self):
        return self.name
    
    def defend(self):
        print("Defend")
        self.defending = True
        self.attacking = True
        self.target.decideNextMove()

    def run(self):
        print("Attack")
        luck = random.randint(1, 100)
        if luck % 2 == 0:
            print("You escaped successfully!")
            self.defending = False
            self.attacking = False
        else:
            print("Your escape attempt failed")
            enemy.decideNextMove()

    def go(self, hcs):
        if not self.attacking:
            if hcs.getContentsOfRoom(self.currentRoom, "str") != "":
                print("You may choose somewhere to visit")
                i = 1
                for place in hcs.getContentsOfRoom(self.currentRoom, "list"):
                    print(str(i) + "). " + place.getName())
                    i += 1
                target = "not an int"
                while not type(target) is int:
                    try:
                        target = int(input("Where would you like to go? (Type 0 for none of these)"))
                    except ValueError as e:
                        print("This input must be a number")
                hcs.getContentsOfRoom(self.currentRoom, "list")[target-1].onVisit(self)
        else: print("You cannot go anywhere whilst attacking")

    def setTarget(self, hcs):
        if hcs.getEnemiesInRoom(self.currentRoom, "str") != "":
            print("You must choose an enemy to target")
            i = 1
            for enemy in hcs.getEnemiesInRoom(self.currentRoom, "list"):
                print(str(i) + "). " + enemy.getName())
                i += 1
            target = "not an int"
            while not type(target) is int:
                try:
                    target = int(input("Who would you like to target?"))
                except ValueError as e:
                    print("This input must be a number")
            self.makeTarget(hcs.getEnemiesInRoom(self.currentRoom, "list")[target-1])
            self.attacking = True

    def explore(self, hcs):
        if not self.attacking:
            choosing = True
            while choosing:
                direction = input("Which way do you want to go? (N/E/S/W)")
                if direction == "N":
                    directionInt = 0
                elif direction == "E":
                    directionInt = 1
                elif direction == "S":
                    directionInt = 2
                elif direction == "W":
                    directionInt = 3
                else:
                    directionInt = 4

                if hcs.findNewRoom(self.currentRoom, directionInt, "str") != "That was not a valid direction" and hcs.findNewRoom(self.currentRoom, directionInt, "str") != "You cannot go in that direction... Please try again.":
                    choosing = False
                    print(hcs.findNewRoom(self.currentRoom, directionInt, "str"))
                if hcs.findNewRoom(self.currentRoom, directionInt, "num") != 0:
                    self.currentRoom = int(hcs.findNewRoom(self.currentRoom, directionInt, "num"))
                print("Enemies in this room: \n" + hcs.getEnemiesInRoom(self.currentRoom, "str"))
                self.setTarget(hcs)
                print("Contents of this room: \n" + hcs.getContentsOfRoom(self.currentRoom, "str"))
        else: print("You cannot explore while attacking... Please run away first")
                    
      

    def helpMe(self):
        print("Commands to choose from are: explore, go, help, status, attack, run, defend, target, quit")

    def getStatus(self):
        print("Your status:")
        print("\nYour armour stats: ")
        for piece in self.armour:
            print(piece.toStats() + "\n")
        print("Your weapon stats: " + self.weapon.toStats())
        print("\nYour remaining HP: " + str(self.hitPoints))

    def quitIt(self):
        print("Quitting")
        quit()

    def doCommand(self, s, hcs):
        if s in hcs.getCommands() and s != "explore" and s != "target" and s != "go":
            hcs.getCommands()[s]()
        elif s in hcs.getCommands():
            hcs.getCommands()[s](hcs)
        else:
            print("Invalid input... Please try again")

    def makeTarget(self, target):
        self.target = target
        print(self.target)

class HardCodedStuff:
    def __init__ (self, _player):
        self.player = _player
        ##REMEMBER: MAX ARMOUR VAL MUST BE 200 OR YOU NEED TO CHANGE EARLIER##
        self.armour = [Armour(1, "Helmet of Beginner's Luck"), Armour(2, "Billy's Helm")]
        self.weapons = [Weapon("Billy's Knife", 10)]
        self.enemies = [Enemy("Billy", 2, self.weapons[0], [self.armour[1]], 10, self.player)]
        self.rooms = [[0,0,0,0],[0, 2, 7, 0], [0, 3, 8, 1], [0, 4, 9, 2], [0, 5, 10, 3],[0, 6, 11, 4], [0, 0, 12, 5], [1, 8, 13, 0], [2, 9, 14, 7],[3, 10, 15, 8], [4, 11, 16, 9], [5, 12, 17, 10], [6, 0, 18, 11],[7, 14, 19, 0], [8, 15, 20, 13], [9, 16, 21, 14], [10, 17, 22, 15], [11, 18, 23, 16], [12, 0, 24, 17], [13, 20, 25, 0], [14, 21, 26, 19], [15, 22, 27, 20], [16, 23, 28, 21], [17, 24, 29, 2], [18, 0, 30, 23], [19, 26, 31, 0], [20, 27, 32, 25], [21, 28, 33, 26], [22, 29, 34, 27], [23, 30, 35, 28], [24, 0, 36, 29], [25, 32, 0, 0], [26, 33, 0, 31], [27, 34, 0, 32], [28, 35, 0, 33], [29, 36, 0, 34], [30, 0, 0, 35]]
        self.descriptions = [Room("You cannot go in that direction... Please try again.", "You cannot go in that direction... Please try again.", []), Room("This is where you were created... The Mii Creation Screen where you, the saviour of your kind, were born", "Story", [MiiRecoverii("1R")]), Room("This is where you were created... The Mii Creation Screen where you, the saviour of your kind, were born2", "Story2", [MiiRecoverii("2R")]), Room("This is where you were created... The Mii Creation Screen where you, the saviour of your kind, were born3", "Story3", [MiiRecoverii("3R")])]
        self.populateCommandsDict()

    def populateCommandsDict(self):
        self.commands = {
            "help": player.helpMe,
            "attack": player.attack,
            "defend": player.defend,
            "explore": player.explore,
            "status": player.getStatus,
            "run": player.run,
            "quit": player.quitIt,
            "go": player.go,
            "target": player.setTarget,
      } 

    def findNewRoom(self, index1, index2, s):
        if index2 == 4:
            return "That was not a valid direction"
        room = self.rooms[index1][index2]
        if s == "str":
            if self.descriptions[room].isVisited():
                return self.descriptions[room].getShortDesc()
            self.descriptions[room].setVisited(True)
            return self.descriptions[room].getLongDesc()
        return room

    def getCommands(self):
        return self.commands

    def getStatsAtIndexInArmourArray(self, index):
        return self.armour[index].toStats()

    def getStatsAtIndexInEnemyArray(self, index):
        return self.enemies[index].getStats()

    def getEnemiesInRoom(self, room, returnType):
        returns = []
        for enemy in self.enemies:
            if not enemy.isDead():
                if enemy.getRoom() == room:
                    if returnType == "str":
                          returns.append(enemy.getStats())
                    else:
                          returns.append(enemy)
        if returnType == "str":
            return str(returns)[1:-1]
        return returns

    def getContentsOfRoom(self, room, returnType):
        returns = []
        for place in self.descriptions[room].getContents():
            if returnType == "str":
                returns.append(place.getName())
            else: returns.append(place)
        if returnType == "str":
            return str(returns)[1:-1]
        return returns
    
class Armour:
    
    def __init__ (self, val, name):
        self.val = val
        self.name = name
    
    def getVal(self):
        return self.val
    
    def getName(self):
        return self.name
    
    def toStats(self):
        return self.name + ": Armour Points: " + str(self.val)
    
class Enemy(Animate):
    
    def __init__ (self, name, room, weapon, armour, hitPoints, player):
        super().__init__(name, room, hitPoints, weapon, armour)
        self.target = player

    def getStats(self):
        return self.name + ": Health: " + str(self.hitPoints)

    def getRoom(self):
        return self.currentRoom

    def getName(self):
        return self.name

    def getHealth(self):
        return self.hitPoints

    def decideNextMove(self):
        luck = random.randint(1, 100)
        if luck % 88 == 0:
            self.run()
        else:
            if luck > 70:
                self.defend()
            else:
                self.attack()

    def takeDamage(self, damagePoints):
        print("Taking damage in enemy")
        ##damage taken is equal to damage given multiplied by (1 - your armour as a percentage of the maximum armour value (200)) and if defending that damage is divided by 2, 3 or 4
        if self.isDefending():
            self.hitPoints -= int((damagePoints * (1 - (self.armourProtection / 200))) / random.randint(2, 4))
        else: self.hitPoints -= int(damagePoints * (1 - (self.armourProtection / 200)))
        if self.hitPoints <= 0:
            self.die()
        else:
            self.decideNextMove()
        print(self.hitPoints)


class Weapon:

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def getDamage(self):
        return self.damage

    def toStats(self):
        return self.name +": Damage Given: " + str(self.damage)

class Room:

    def __init__(self, shortDesc, longDesc, contents):
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        self.contents = contents
        self.visited = False

    def isVisited(self):
        return self.visited

    def setVisited(self, boolean):
        self.visited = boolean

    def getShortDesc(self):
        return self.shortDesc

    def getLongDesc(self):
        return self.longDesc

    def getContents(self):
        return self.contents

class Place:
    
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

class MiiRecoverii(Place):

    def __init__(self, name):
        super().__init__(name)

    def onVisit(self, player):
        while True:
            heal = input("Welcome to MiiRecoverii! Would you like to be healed? (Y/N)").upper()
            if heal == "Y":
                print("3")
                time.sleep(1)
                print("2")
                time.sleep(1)
                print("1...Aaaaand voila! You have been healed")
                player.hitPoints = player.fullHitPoints
                break
            elif heal == "N":
                print("See you soon then!")
                break
            else:
                print("I'm sorry... I don't understand you...")

        
    
player = Player(input("Hello Player! What's your name?\n>>>"))
print("Hello there " + player.getName())
hcs = HardCodedStuff(player)
print("Your armour stats: " + hcs.getStatsAtIndexInArmourArray(0))
playing = True
while playing:
    s = input(">>>").lower()
    player.doCommand(s, hcs)
