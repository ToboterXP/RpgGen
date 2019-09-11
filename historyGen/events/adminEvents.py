from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import random as r
import copy


class HEvBecomeAdmin(HistoricEvent):
    def __init__(self,pos,time,context):
        self.character = None
        for c in context.getHistoryMap().getCharacters():
            if (c.getCurrentState().alive
                and c.getAge(time)>=c.getCurrentState().getRace().adultAge
                and c.getCurrentState().getAttributes().getMind() >= r.randint(5,12)
                and c.getCurrentState().getPersonality().determination >= r.randint(5,15)
                and (not c.getCurrentState().noLeader)
                and (not c.getCurrentState().livingPlace.getCurrentState().leader)):
                self.character = c
                break

        if not self.character:
            self.setSuccessful(False)
            return

        self.location = self.character.getCurrentState().livingPlace
        super().__init__(self.location.getPos(),time,[self.character],
                         context,[self.location])
        self.updateCharacters()
        self.updateLocations()

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.leader = self.character
            return newState
        return state

    def getModifiedCharacterState(self,character,state):
        if character == self.character:
            newState = copy.copy(state)
            newState.leadershipPos = self.location
            return newState
        return state

    def getDescription(self,character):
        return "%s assumed leadership of %s in %i" % (self.character.getName(),self.location.getName(),self.getTime())

    def getLocationDescription(self,location):
        return self.getDescription(self.character)

class HEvResignAsAdmin(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)
        self.character = None
        for c in characters:
            if (c.getCurrentState().alive
                and c.getCurrentState().leadershipPos):
                self.character = c
                break

        if not self.character:
            self.setSuccessful(False)
            return

        if self.character.getPersonality().determination>r.randint(1,8):
            self.setSuccessful(False)
            return

        self.location = self.character.getCurrentState().livingPlace
        super().__init__(self.location.getPos(),time,[self.character],
                         context,[self.location])
        self.updateCharacters()
        self.updateLocations()

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.leader = None
            return newState
        return state

    def getModifiedCharacterState(self,character,state):
        if character == self.character:
            newState = copy.copy(state)
            newState.leadershipPos = None
            newState.noLeader = True
            return newState
        return state

    def getDescription(self,character):
        return "%s resigned as leader of %s in %i" % (self.character.getName(),self.location.getName(),self.getTime())

    def getLocationDescription(self,location):
        return self.getDescription(self.character)

class HEvAssassinateLeader(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)
        self.character = None
        for c in characters:
            if (c.getCurrentState().alive
                and c.getAge(time)>=c.getCurrentState().getRace().adultAge
                and c.getCurrentState().livingPlace.getCurrentState().leader
                and not c.getCurrentState().leadershipPos):
                self.character = c
                break

        if not self.character:
            self.setSuccessful(False)
            return

        self.target = self.character.getCurrentState().livingPlace.getCurrentState().leader

        if ((not self.target.getPersonality().extreme)
            and (self.target.getPersonality().determination<r.randint(5,15))):

            self.setSuccessful(False)
            return
            

        if (self.character.getPersonality().determination<r.randint(5,15)
            or self.character.getPersonality().warmonger<r.randint(5,15)):
            self.setSuccessful(False)
            return

        self.location = self.character.getCurrentState().livingPlace
        self.stolenItems = self.target.getCurrentState().items
        super().__init__(self.location.getPos(),time,[self.character,self.target],
                         context,[self.location])
        self.updateCharacters()
        self.updateLocations()

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.leader = None
            return newState
        return state

    def getModifiedCharacterState(self,character,state):
        if character == self.character:
            newState = copy.copy(state)
            newState.items += self.stolenItems
            return newState
        if character == self.target:
            newState = copy.copy(state)
            newState.alive = False
            newState.items = []
            newState.leadershipPos = None
            return newState
        return state

    def getDescription(self,character):
        if character == self.target:
            return "%s was assassinated by %s in %i" % (self.target.getName(),self.character.getName(),self.getTime())
        if character == self.character:
            return "%s assassinated %s in %i" % (self.character.getName(),self.target.getName(),self.getTime())

    def getLocationDescription(self,location):
        return self.getDescription(self.target)

