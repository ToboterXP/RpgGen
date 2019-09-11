from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import random as r
import copy

class HEvBirth(HistoricEvent):
    def __init__(self,pos,time,context):
        newCharacter = HistoricCharacter(self)
        
        self.attributes = CharacterAttributes.generateRandom(r.randint(17,20))
        if r.random()>=0.1:
            self.race = context.getRacialMap().getClosest(pos).getObject().getName()
        else:
            self.race = r.choice(context.getRacialMap().getNodes()).getObject().getName()

        self.livingPlace = context.getClosestLocation(
            pos,sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().livable).getAttachedContext(HistoryLocation)
        
        super().__init__(self.livingPlace.getPos(),time,[newCharacter],context,[self.livingPlace])
        context.getHistoryMap().addCharacter(newCharacter)
        
        self.name = "Person"+str(context.getHistoryMap().getCharacters().index(newCharacter))
        self.personality = CharacterState.generatePersonality()
        
        self.updateCharacters()
        self.updateLocations()
        
    def getModifiedCharacterState(self,character,state):
        if character == self.getCharacters()[0]:
            livingPlace = self.livingPlace
            self.pos = livingPlace.getPos()
            newState = copy.copy(state)
            newState.livingPlace = livingPlace
            newState.alive = True
            newState.attributes = self.attributes
            newState.race = self.race
            newState.name = self.name
            newState.personalityTraits = self.personality
            return newState
        return state

    def getModifiedLocationState(self,location,state):
        if location == self.livingPlace:
            newState = copy.copy(state)
            newState.characters += [self.getCharacters()[0]]
            newState.associatedCharacters += [self.getCharacters()[0]]
            return newState
        return state

    def getDescription(self, character):
        if character == self.getCharacters()[0]:
            return "%s was born in %i in %s" % (character.getName(),self.getTime(),self.livingPlace.getName())
        return ""

    def getLocationDescription(self,location):
        return self.getDescription(self.getCharacters()[0])



class HEvUnspecifiedDeath(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)

        char = None
        age = 0
        for c in characters:
            newAge = (time - c.getBirthTime())
            if  newAge>age and c.getCurrentState().alive:
                age = newAge
                char = c

        if not char or age<r.randint(c.getCurrentState().getRace().oldAge,c.getCurrentState().getRace().maxAge):
            self.setSuccessful(False)
            return

        self.character =char
        self.location = char.getCurrentState().livingPlace
        self.items = char.getCurrentState().items

        super().__init__(char.getCurrentState().livingPlace.getPos(),time,[char],context,[char.getCurrentState().livingPlace])
        self.updateCharacters()
        self.updateLocations()

    def getModifiedCharacterState(self,character,state):
        if character == self.getCharacters()[0]:
            newState = copy.copy(state)
            newState.alive = False
            newState.items = []
            newState.leadershipPos = None
            return newState
        return state

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.storedItems += self.items
            if self.character == newState.leader:
                newState.leader = None
            return newState
        return state

    def getDescription(self,character):
        items = ""
        for i in self.items:
            items += "\n"+i.getName()
        return "%s died in %i leaving %s" % (character.getName(),self.getTime(),items)

    def getLocationDescription(self,location):
        return self.getDescription(self.getCharacters()[0])
