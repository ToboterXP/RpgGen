from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import random as r
import copy

class HEvChooseProfession(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        
        char = None
        for c in characters:
            if c.getAge(time)>=c.getCurrentState().getRace().adultAge and c.getCurrentState().occupation == CharacterOccupationPreset.NONE:
                char = c
                break

        if not char:
            self.setSuccessful(False)
            return
        

        self.occupation = r.choice(CharacterOccupationPreset.PROFESSIONS)
        super().__init__(char.getCurrentState().livingPlace.getPos(),time,[char],context)
        self.updateCharacters()

    def getModifiedCharacterState(self,character,state):
        if character == self.getCharacters()[0]:
            newState = copy.copy(state)
            newState.occupation = self.occupation
            newState.occupationLevel = 1
            return newState
        return state

    def getDescription(self,character):
        return "%s took the occupation %s in %i" % (character.getName(),self.occupation.name,self.getTime())



class HEvImproveAtProfession(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)
        
        char = None
        for c in characters:
            if c.getCurrentState().alive and c.getCurrentState().occupation != CharacterOccupationPreset.NONE:
                char = c
                break

        if not char:
            self.setSuccessful(False)
            return

        super().__init__(char.getCurrentState().livingPlace.getPos(),time,[char],context)
        self.updateCharacters()

    def getModifiedCharacterState(self,character,state):
        if character == self.getCharacters()[0]:
            newState = copy.copy(state)
            newState.occupationLevel += 1
            return newState
        return state

    def getDescription(self,character):
        return "%s improved in %i" % (character.getName(),self.getTime())
