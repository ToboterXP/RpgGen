from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import randomUtil as r
import copy

class HEvTravel(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)
        
        char = None
        for c in characters:
            if (c.getAge(time)>=c.getCurrentState().getRace().adultAge
                and c.getCurrentState().alive
                and c.getCurrentState().traveling>=r.randint(1,21)
                and c.getCurrentState().getPersonality().determination >= r.randint(1,15)
                and (not c.getCurrentState().leadershipPos)):
                
                char = c
                break

        if not char:
            self.setSuccessful(False)
            return

        possible = None
        if c.getCurrentState().traveling>=r.randint(1,31):
            possible = context.getCloseLocations(pos,5,sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().livable)
        else:
            possible = context.getCloseLocations(pos,5,sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().independant)

        possibleLocs = []
        for p in possible:
            possibleLocs.append(p.getAttachedContext(HistoryLocation))

        if r.random()<0.3:
            self.target = r.choice(possibleLocs)
        else:
            popCount = []
            self.target = max(possibleLocs,key=lambda p: len(p.getCurrentCharacters(time)))

        self.prevLoc = char.getCurrentState().livingPlace
        super().__init__(self.target.getPos(),time,[char],context,[self.target,self.prevLoc])
        self.updateCharacters()
        self.updateLocations()

    def getModifiedCharacterState(self,character,state):
        if character == self.getCharacters()[0]:
            newState = copy.copy(state)
            newState.livingPlace = self.target
            return newState
        return state

    def getModifiedLocationState(self,location,state):
        if location == self.target:
            newState = copy.copy(state)
            newState.characters += [self.getCharacters()[0]]
            return newState
        return state

    def getDescription(self,character,verb="traveled"):
        return "%s %s to %s in %i" % (character.getName(),verb,self.target.getName(),self.getTime())

    def getLocationDescription(self,location):
        if location == self.target:
            return self.getDescription(self.getCharacters()[0])
        else:
            return self.getDescription(self.getCharacters()[0],"departed")

class HEvFoundLocation(HistoricEvent):
    def __init__(self,pos,time,context):
        self.location = None
        locations = context.getHistoryMap().getLocations()
        r.shuffle(locations)

        for l in locations:
            if not l.getCurrentState().existing:
                self.location = l
                break

        if not self.location:
            self.setSuccessful(False)
            return

        assert not self.location.getCurrentState().existing

        possible = context.getCloseLocations(self.location.getPos(),5,sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().independant)
        self.admin = None
        for p in possible:
            if (p.getAttachedContext(HistoryLocation).getLocationType().size
                >= self.location.getLocationType().size
                and p.getAttachedContext(HistoryLocation).getPersonality().determination >= r.randint(1,10)):
                self.admin = p.getAttachedContext(HistoryLocation)
                break

        locs = [self.location,self.admin] if self.admin else [self.location]
        super().__init__(self.location.getPos(),time,[],context,locs)
        self.updateLocations()

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.existing = True
            newState.adminLocation = self.admin
            return newState
        if location == self.admin:
            newState = copy.copy(state)
            newState.subordinateLocs.append(self.location)
            return newState
        return state

    def getLocationDescription(self,location):
        if location == self.location:
            founding = ""
            if self.admin:
                founding = "by %s" % (self.admin.getName())
            return "%s was founded in %i %s" % (location.getName(),self.getTime(),founding)
        elif location == self.admin:
            return "%s founded %s in %i" % (location.getName(),self.location.getName(),self.getTime())

class HEvActiveFoundLocation(HistoricEvent):
    def __init__(self,pos,time,context):
        self.location = None
        locations = context.getHistoryMap().getLocations()
        r.shuffle(locations)

        for l in locations:
            if not l.getCurrentState().existing:
                self.location = l
                break

        if not self.location:
            self.setSuccessful(False)
            return

        possFounderSource = context.getCloseLocations(self.location.getPos(),5,sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().livable)

        possFounders = []
        for p in possFounderSource:
            possFounders += p.getAttachedContext(HistoryLocation).getCurrentCharacters(time)

        founder = None
        legendarity = 0
        for f in possFounders:
            if (f.getAge(time)>=f.getCurrentState().getRace().adultAge
                and (not f.getCurrentState().leadershipPos)
                and f.getLegendarity()>=r.randint(4,15)
                and f.getCurrentState().getPersonality().determination >= r.randint(1,15)
                and f.getLegendarity()>=legendarity  ):

                founder = f
                legendarity = f.getLegendarity()

        if not founder:
            self.setSuccessful(False)
            return

        self.founder = founder
        self.founderHome = self.founder.getCurrentState().livingPlace

        super().__init__(self.location.getPos(),time,[self.founder],context,[self.location,self.founderHome])
        self.updateLocations()
        self.updateCharacters()

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.existing = True
            newState.characters += [self.getCharacters()[0]]
            newState.adminLocation = self.founderHome
            newState.leader = self.founder
            return newState
        elif location == self.founderHome:
            newState = copy.copy(state)
            newState.subordinateLocs.append(self.location)
            return newState
        return state

    def getModifiedCharacterState(self,character,state):
        if character == self.founder:
            newState = copy.copy(state)
            newState.livingPlace = self.location
            newState.leadershipPos = self.location
            return newState
        return state

    def getDescription(self,character):
        return "%s founded %s in %i" % (character.getName(),self.location.getName(),self.getTime())

    def getLocationDescription(self,location):
        if location == self.location:
            return "%s was founded in %i by %s" % (self.location.getName(),self.getTime(),self.founder.getName())
        else:
            return "%s left to found %s in %i" % (self.founder.getName(),self.location.getName(),self.getTime())
