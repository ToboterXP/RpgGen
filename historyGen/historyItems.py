import random as r

class CharacterAttributes:
    def __init__(self,body=6,agility=6,mind=6):
        self.body = body
        self.agility = agility
        self.mind = mind

    def getBody(self):
        return self.body

    def getAgility(self):
        return self.agility

    def getMind(self):
        return self.mind

    def generateRandom(proficiency=20):
        values = [0,0,0]
        for i in range(proficiency):
            n = r.randint(0,2)
            while values[n]>=8 and not r.random()<0.1:
                n = r.randint(0,2)

            values[n] += 1

        return CharacterAttributes(*values)

    def applyModifier(self,attributes):
        self.body += attributes.getBody()
        self.agility += attributes.getAgility()
        self.mind += attributes.getMind()

    def difference(self,other):
        return abs(self.getBody()-other.getBody()) + abs(self.getAgility()-other.getAgility()) + abs(self.getMind()-other.getMind())

    def __str__(self):
        return "BOD: %i AGI: %i MIN: %i" % (self.body,self.agility,self.mind)

class HistoryItem:
    def __init__(self,quality,weapon=False,art=False,attrMod=CharacterAttributes(0,0,0)):
        self.weapon =weapon
        self.art = art
        self.attrMod = attrMod
        self.name = ""
        self.quality = quality

    def getName(self):
        return self.name

ITEM_NUMBER = 0

class HIWeapon(HistoryItem):
    def __init__(self,quality):
        global ITEM_NUMBER
        super().__init__(quality,weapon=True,attrMod=CharacterAttributes(quality+r.randint(0,1),0,0))
        self.name = "Weapon"+str(ITEM_NUMBER)
        ITEM_NUMBER += 1

class HIWovenArt(HistoryItem):
    def __init__(self,quality):
        global ITEM_NUMBER
        super().__init__(quality,art=True)
        self.name = "Carpet"+str(ITEM_NUMBER)
        ITEM_NUMBER += 1
