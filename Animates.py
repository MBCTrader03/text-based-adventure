from Inanimates import *
import random

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
        print(self.name + " attacks " + self.target.getName())
        self.attacking = True
        self.defending = False
        self.target.takeDamage(random.randint(self.weapon.getDamage()-2, self.weapon.getDamage()+2))

    ##All Animate objects have a way of defending
    def defend(self):
        if self.defending:
            print(self.name + " continues to defend")
        else: print(self.name + " is now defending")
        self.defending = True
        self.attacking = True

    ##All Animate objects have a way of running
    def run(self):
        print(self.name + " attempts to run from " + self.target.getName())
        luck = random.randing(1, 100)
        if luck % 2 == 0:
            print(self.name + " has escaped successfully!")
            self.defending = False
            self.attacking = False
        else: print(self.name + "'s escape attempt failed")

    def takeDamage(self, damagePoints):
        ##damage taken is equal to damage given multiplied by (1 - your armour as a percentage of the maximum armour value (200)) and if defending that damage is divided by 2, 3 or 4
        if self.isDefending():
            myDamage = int((damagePoints * (1 - (self.armourProtection / 200))) / random.randint(2, 4))
            self.hitPoints -= myDamage
        else:
            myDamage = int(damagePoints * (1 - (self.armourProtection / 200)))
            self.hitPoints -= myDamage
        print(self.name + " took " + str(myDamage) + " damage")
        if self.hitPoints <= 0:
            self.die()
            self.target.setAttacking(False)
            print(self.name + " died")
        else:
            if self.hitPoints > 1: print(self.name + " has " + str(self.hitPoints) + " hit points remaining")
            else: print(self.name + " has " + str(self.hitPoints) + " hit point remaining")
            
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

    def setAttacking(self, boolean):
        self.attacking = boolean

class Player(Animate):
    
    def __init__(self, name):
        super().__init__(name, 1, 100, Weapon("Hands",  5), [Armour(1, "Helmet of Beginner's Luck")])
        self.fullHitPoints = 100
    
    def getName(self):
        return self.name
    
    def defend(self):
        if self.defending:
            print(self.name + " continues to defend")
        else: print(self.name + " is now defending")
        self.defending = True
        self.attacking = True
        self.target.decideNextMove()

    def run(self):
        print(self.name + " attempts to run from " + self.target.getName())
        luck = random.randing(1, 100)
        if luck % 2 == 0:
            print(self.name + " has escaped successfully!")
            self.defending = False
            self.attacking = False
        else:
            print(self.name + "'s escape attempt failed")
            target.decideMextMove()

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
        ##damage taken is equal to damage given multiplied by (1 - your armour as a percentage of the maximum armour value (200)) and if defending that damage is divided by 2, 3 or 4
        if self.isDefending():
            myDamage = int((damagePoints * (1 - (self.armourProtection / 200))) / random.randint(2, 4))
            self.hitPoints -= myDamage
        else:
            myDamage = int(damagePoints * (1 - (self.armourProtection / 200)))
            self.hitPoints -= myDamage
        print(self.name + " took " + str(myDamage) + " damage")
        if self.hitPoints <= 0:
            self.die()
            self.target.setAttacking(False)
            print(self.name + " died")
        else:
            self.decideNextMove()
            if self.hitPoints > 1: print(self.name + " has " + str(self.hitPoints) + " hit points remaining")
            else: print(self.name + " has " + str(self.hitPoints) + " hit point remaining")