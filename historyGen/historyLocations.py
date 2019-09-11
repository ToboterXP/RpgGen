import random as r
from historyGen.historyCharacters import CHARACTER_RACES,PersonalityTraits

class LocationState:
    def __init__(self,existing,name):
        self.characters = []
        self.associatedCharacters = []
        self.name = name
        self.existing = existing
        self.storedItems = []
        
        self.adminLocation = None
        self.subordinateLocs = []
        self.lostLocations = []
        self.friendlyLocations = []
        self.leader = None
        self.race = None

    def getPersonality(self):
        if self.leader:
            return self.leader.getCurrentState().getPersonality()
        else:
            return PersonalityTraits.BASIC

    def __str__(self):
        charList = ""
        for c in self.characters:
            charList += c.getName()+"\n"

        adminLoc = self.adminLocation.getName() if self.adminLocation else "None"
        

        subLocs = ""
        for s in self.subordinateLocs:
            subLocs += "\n"+s.getName()
        return """Name: %s
AdminLocation: %s
SubLocations: %s
LocalRace: %s
Inhabitants: %s""" % (self.name, adminLoc,subLocs,self.race,charList)

class HistoryLocation:
    def __init__(self,node,context,existing = False,name=""):
        self.node = node
        self.context = context
        node.attachContext(self)
        self.events = []
        self.state = LocationState(existing,name)
        self.ancient = existing
        self.locationType = HISTORIC_LOCATION_TYPE[node.getObject().getName()]
        if not self.locationType.foundable:
            self.state.existing = True
            self.ancient = True

        self.localRace = context.getRacialMap().getClosest(self.node.getPos())
        self.state.race = self.localRace.getObject().getName()
        self.localRace = CHARACTER_RACES[self.localRace.getObject().getName()]
        
        if self.localRace.imperial and self.state.existing and self.locationType.independant:
            for locNode in (context.getCivilLocMap().getMultipleClosest(self.node.getPos(),5)
                            +context.getGeneralLocMap().getMultipleClosest(self.node.getPos(),5)):

                if locNode == self.node:
                    continue
                loc = None
                try:
                    loc = locNode.getAttachedContext(HistoryLocation)
                except:
                    continue
                
                if (loc.getLocationType().foundable
                    and (loc.getLocalRace().imperial or (not loc.getLocationType().independant))
                    and loc.getLocalRace()==self.localRace
                    and (not loc.getCurrentState().adminLocation)
                    and loc.getCurrentState().existing):
                    if loc.getLocationType().size < self.getLocationType().size:
                        loc.setAdminLocation(self)
                    elif loc.getLocationType().size > self.getLocationType().size:
                        self.setAdminLocation(loc)
                        break
                    else:
                        if r.random()<0.5:
                            loc.setAdminLocation(self)
                        else:
                            self.setAdminLocation(loc)
                            break

    def getLocalRace(self):
        return self.localRace

    def getPersonality(self):
        return self.state.getPersonality()

    def _addSubordinate(self,loc):
        self.state.subordinateLocs.append(loc)

    def _removeSubordinate(self,loc):
        self.state.subordinateLocs.remove(loc)
        
    def setAdminLocation(self,loc,malicious=True):
        if self.state.adminLocation:
            self.state.adminLocation._removeSubordinate(self)
        self.state.adminLocation = loc
        loc._addSubordinate(self)

    def getMainAdmin(self):
        if self.state.adminLocation:
            return self.state.adminLocation.getMainAdmin()
        else:
            return self

    def getLocationType(self):
        return self.locationType

    def destroy(self,context):
        context.getHistoryMap().getLocations().remove(self)
        try:
            context.getCivilLocMap().removeNode(self.node)
        except:
            context.getGeneralLocMap().removeNode(self.node)

    def addEvent(self,event):
        self.events.append(event)
        self.state = event.getModifiedLocationState(self,self.getCurrentState())
        self.getMainAdmin()

    def getPos(self):
        return self.node.getPos()
    
    def getCurrentState(self):
        return self.state

    def getCurrentCharacters(self,time,minors=False):
        ret = []
        for c in self.state.characters:
            if c.getCurrentState().livingPlace == self and c.getCurrentState().alive and (minors or c.getAge(time)>=c.getCurrentState().getRace().adultAge):
                ret.append(c)
        return ret

    def getName(self):
        return self.getCurrentState().name

    def getCreationTime(self):
        if self.ancient:
            return 0
        else:
            try:
                return self.events[0].getTime()
            except:
                return -10

    def getEventDescriptions(self):
        rets = [str(self.getCurrentState())]
        for event in self.events:
            rets.append(event.getLocationDescription(self))
        return rets

class HistoricLocationType:
    def __init__(self,foundable=False,livable=False,independant=False,size=1):
        self.foundable = foundable
        self.livable = livable
        self.independant = independant
        self.size = size

HISTORIC_LOCATION_TYPE = {
    "Village":HistoricLocationType(True,True,True,size=3),
    "City":HistoricLocationType(True,True,True,size=5),
    "MountainHome":HistoricLocationType(True,True,True,size=4),
    "TreeCity":HistoricLocationType(True,True,True,size=4),
    "Farm":HistoricLocationType(True,True),
    "GuardTower":HistoricLocationType(True),
    "Mine":HistoricLocationType(True),
    "Castle":HistoricLocationType(True,True,True,size=2),
    "Ruin":HistoricLocationType(),
    "Cave":HistoricLocationType()
    }
