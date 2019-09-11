from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import random as r
import copy

class HistoricMapContext:
    def __init__(self, fineMap, racialMap, civilLocMap, generalLocMap, historyMap):
        self.fineMap = fineMap
        self.racialMap = racialMap
        self.civilLocMap = civilLocMap
        self.generalLocMap = generalLocMap
        self.historyMap = historyMap

    def getFineBiomeMap(self):
        return self.fineMap

    def getRacialMap(self):
        return self.racialMap

    def getCivilLocMap(self):
        return self.civilLocMap

    def getGeneralLocMap(self):
        return self.generalLocMap

    def getHistoryMap(self):
        return self.historyMap

    def getCloseLocations(self,pos,num=1,sort=None):
        fullSort = lambda n: sort(n) and n.getAttachedContext(HistoryLocation).getCurrentState().existing
        possible = self.civilLocMap.getMultipleClosest(pos,num,fullSort)
        possible += self.generalLocMap.getMultipleClosest(pos,num,fullSort)
        
        possible.sort(key=lambda n: abs(pos-n.getPos()))
        return possible[:num]

    def getClosestLocation(self,pos,sort=None):
        return self.getCloseLocations(pos,sort=sort)[0]

class HistoryMap:
    def __init__(self,size):
        self.size = size
        self.events = []
        self.characters = []
        self.items = []
        self.locations = []

    def addEvent(self,event):
        self.events.append(event)

    def addCharacter(self,char):
        self.characters.append(char)

    def addLocation(self,loc):
        self.locations.append(loc)

    def addItem(self,item):
        self.items.append(item)

    def getCharacters(self):
        return self.characters

    def getEvents(self):
        return self.events

    def getItems(self):
        return self.items

    def getLocations(self):
        return self.locations

class HistoricEvent:
    def __init__(self,pos,time,characters,context,locations=[]):
        self.pos = pos
        self.time = time
        self.previous = []
        self.results = []
        self.characters = characters
        self.locations = locations
        self.context = context
        self.successful = True
        self.alternateEvent = None

    def updateCharacters(self):
        for char in self.characters:
            char.addEvent(self)

    def getCharacters(self):
        return self.characters

    def getAlternateEvent(self):
        try:
            return self.alternateEvent
        except:
            return None

    def setAlternateEvent(self,event):
        self.alternateEvent = event

    def updateLocations(self):
        for loc in self.locations:
            loc.addEvent(self)

    def getContext(self):
        return self.context

    def _addPrevious(self,event):
        self.previous.append(event)

    def getTime(self):
        return self.time

    def setSuccessful(self,succ):
        self.successful = succ

    def getSuccessful(self):
        return self.successful

    def addResult(self,event):
        self.results.append(event)
        event._addPrevious(self)

    def getModifiedCharacterState(self,character,state):
        return state

    def getModifiedLocationState(self,location,state):
        return state

    def getLocationDescription(self, location):
        return ""
