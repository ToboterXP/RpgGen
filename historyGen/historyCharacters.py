from historyGen.historyItems import *
import random as r
import copy

class PersonalityTrait:
    def __init__(self,name,warmonger=0,determination=0,extreme=False):
        self.warmonger = warmonger
        self.determination = determination
        self.extreme = extreme
        self.name = name

    def __add__(self,other):
        if not other.__class__ == PersonalityTrait:
            return self
        return PersonalityTrait("",self.warmonger+other.warmonger,
                                self.determination+other.determination,
                                self.extreme or other.extreme)

class PersonalityTraits:
    BASIC = PersonalityTrait("Basic",warmonger=8,determination=8)
    
    AGGRESSIVE = PersonalityTrait("Aggressive",warmonger=4)
    DETERMINATION = PersonalityTrait("Determination",determination=4)
    INSECURE = PersonalityTrait("Insecurity",determination=-2)
    IMPULSIVE = PersonalityTrait("Impulsive",warmonger=2)
    PEACEFUL = PersonalityTrait("Peaceful",warmonger=-3)

    VENGEFUL = PersonalityTrait("Vengeful",warmonger=8,extreme=True)
    STUBBORN = PersonalityTrait("Stubborn",determination=8,extreme=True)
    WEAK_MINDED = PersonalityTrait("Weak Mind",determination=-6,extreme=True)
    

    COMMON_TRAITS = [DETERMINATION,INSECURE,IMPULSIVE,PEACEFUL,AGGRESSIVE]

    TRAUMATIC_TRAITS = [AGGRESSIVE,VENGEFUL,STUBBORN,WEAK_MINDED]
    
    

class CharacterState:
    def __init__(self):
        self.livingPlace = None
        self.alive = None
        self.name = ""
        self.attributes = None
        self.race = None
        self.occupation = CharacterOccupationPreset.NONE
        self.occupationLevel = 1
        self.leadershipPos = None
        self.noLeader = False
        self.traveling = r.randint(1,20)
        self.items = []
        self.itemsOnSale = []
        self.personalityTraits = []

    def getPersonality(self):
        ret = self.personalityTraits[0]
        for trait in self.personalityTraits[1:]:
            ret += trait
        return ret

    def generatePersonality():
        traits = [PersonalityTraits.BASIC]
        traits.append(r.choice(PersonalityTraits.COMMON_TRAITS))
        return traits

    def getRace(self):
        return CHARACTER_RACES[self.race]
    
    def getAttributes(self):
        ret = copy.copy(self.attributes)
        for i in self.items:
            ret.applyModifier(i.attrMod)
        return ret
    
    def __str__(self):
        personality = ""
        for trait in self.personalityTraits:
            personality += trait.name+"\n"
        currPers = self.getPersonality()
        personality += "DETER: %i\nAGGR: %i" % (currPers.determination,currPers.warmonger)
        return """Name: %s
Race: %s
LivingPlace: %s
Attributes: %s
PersonalityTraits: %s
""" % (self.name, self.race, self.livingPlace.getName(), self.attributes,personality)

class CharacterOccupation:
    def __init__(self,name,perfectAttributes,
                 warrior=False,craftsman=False,creationType=None):
        self.name = name
        self.perfectAttributes = perfectAttributes
        self.warrior = warrior
        self.craftsman = craftsman
        self.creationType = creationType

class CharacterOccupationPreset:
    NONE = CharacterOccupation("None",CharacterAttributes(0,0,0))
    
    SOLDIER = CharacterOccupation("Soldier",
                                  CharacterAttributes(8,6,4),
                                  warrior = True)
    SMITH = CharacterOccupation("Smith",
                                CharacterAttributes(7,4,7),
                                craftsman = True,
                                creationType=HIWeapon
                                )
    WEAVER = CharacterOccupation("Weaver",
                                 CharacterAttributes(4,7,8),
                                 craftsman = True,
                                 creationType=HIWovenArt)
    FARMER = CharacterOccupation("Farmer",
                                 CharacterAttributes(8,4,4))

    PROFESSIONS = [SOLDIER,SMITH]

class HistoricCharacter:
    def __init__(self,birthEvent):
        self.modifyingEvents = []
        self.currentState = CharacterState()
        
    def addEvent(self,event):
        self.modifyingEvents.append(event)
        self.currentState = event.getModifiedCharacterState(self,self.currentState)

    def getEvents(self):
        return self.modifyingEvents

    def getCurrentState(self):
        return self.currentState

    def getPersonality(self):
        return self.getCurrentState().getPersonality()

    def getName(self):
        return self.getCurrentState().name

    def getBirthTime(self):
        return self.modifyingEvents[0].getTime()

    def getAge(self,time):
        return time - self.getBirthTime()

    def getLegendarity(self):
        return len(self.getEvents())

    def getEventDescriptions(self):
        ret = [str(self.getCurrentState())]
        for event in self.modifyingEvents:
            ret.append(event.getDescription(self))
        return ret

class CharacterRace:
    def __init__(self,maxAge,oldAge,adultAge,imperial):
        self.maxAge = maxAge
        self.oldAge = oldAge
        self.adultAge = adultAge
        self.imperial = imperial

CHARACTER_RACES= {
    "ImperialHumans" : CharacterRace(80,50,15,True),
    "BarbaricHumans" : CharacterRace(80,50,15,False),
    "Dwarfs" : CharacterRace(120,90,25,True),
    "Elves" : CharacterRace(120,90,25,True),
    "WildElves" : CharacterRace(100,60,20,False),
    "Halflings" : CharacterRace(60,40,10,False)
    }
