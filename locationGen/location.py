import randomUtil as r
import randomTextTemplate as rtt
import copy
from util import *
from locationGen.locationProperty import *
from game.game import Game

class Location:
    def __init__(self,type,given,seed,superLocation,pos=Vector2(0,0),propertyTemplates=[]):
        self.seed = seed
        self.pos = pos
        self.type = type
        self.given = given
        self.taken = []
        self.subLocations = []
        self.connections = []
        self.objects = []
        self.superLocation = superLocation

        self.isLoaded = False
        self.topLocation = False

        self.properties = [t.instantiate(self) for t in propertyTemplates]

    def setAsTopLocation(self):
        self.topLocation = True

    def isTopLocation(self):
        return self.topLocation

    def getTopLocation(self):
        if self.isTopLocation():
            return self
        else:
            return self.superLocation.getTopLocation()

    def getFirstRoom(self):
        if self.subLocations:
            return self.subLocations[0].getFirstRoom()
        else:
            return self

    def getInteractionHandles(self):
        ret = {}
        for p in self.getProperties(LocationPropertyType.LPT_INTERACTIONS):
            ret.update(p.getInteractionHandles())

        return ret

    def getProperties(self,type):
        for p in self.properties:
            if type in p.getTypes():
                yield p

    def getContexts(self,type):
        for p in self.properties:
            if LocationPropertyType.LPT_CONTEXT in p.getTypes() and type==p.getContextName():
                yield p.getContext()

    def getLocationName(self):
        return list(self.getContexts("HistoryLocation"))[0].getCurrentState().name

    def attachProperty(self,prop):
        self.properties.append(prop.instantiate(self))

    def getPos(self):
        return self.pos

    def setPos(self,pos):
        self.pos = pos

    def isConnection(self):
        return False

    def addConnection(self,conn):
        self.connections.append(conn)

    def removeConnection(self,conn):
        self.connections.remove(conn)

    def getConnections(self):
        return self.connections

    def addObject(self,obj):
        self.objects.append(obj)

    def removeObject(self,obj):
        self.objects.remove(obj)

    def getObjects(self):
        return self.objects

    def getSubLocations(self):
        return self.subLocations

    def getType(self):
        return self.type

    def loadContent(self):
        if self.isLoaded:
            return
        self.isLoaded = True

        r.pushSeed(self.seed)
        self.subLocations = self.type.rootContentCollection.generateLocations(self.given,self.taken,self.connections,self)
        for loc in self.subLocations:
            loc.loadContent()
        r.popSeed()

    def unloadContent(self,deleteConns=False):
        if not self.isLoaded:
            return
        self.isLoaded = False

        for sl in self.subLocations[:]:
            sl.unloadContent(True)
            del sl
        if deleteConns:
            for c in self.connections[:]:
                c.delete()
        self.given += self.taken
        self.taken = []
        self.subLocations = []

    def getProperties(self,tag):
        for p in self.properties:
            if tag in p.getTypes():
                yield p

    def getDescription(self):
        ret = ""
        descProps = list(self.getProperties(LocationPropertyType.LPT_DESCRIPTION))
        descProps.sort(key=lambda p: p.getDescPrority())
        for p in descProps:
            ret += p.getDescription() + "\n\n"

        return ret[:-2]

    def getName(self):
        name = ""
        for p in self.getProperties(LocationPropertyType.LPT_DESCRIPTION):
            if p.getLocationName() != "":
                name = p.getLocationName()
        return name

    def printSubLocations(self,prefix="",start=True,inDepth = False):
        if start:
            print(self.getLocationName(),self.type.name,self.pos)
        for sl in self.subLocations:
            i = self.subLocations.index(sl)
            connections = ""
            for c in sl.getConnections():
                cLoc = c.getOther(sl)
                if cLoc in self.subLocations:
                    connections += str(self.subLocations.index(cLoc))+", "
                elif cLoc == self:
                    connections += "A"+str(self.connections.index(c.getLocationConnection(self)))+", "
                elif cLoc in sl.getSubLocations():
                    connections += "V"+str(sl.getSubLocations().index(cLoc))+", "
                else:
                    connections += "X, "
            connections = "("+connections[:-2]+")"
            print(prefix+str(i)+".", sl.getDescription()+"("+sl.getName()+")" ,connections,sl.getPos(),end=" ")
            if inDepth:
                print(sl,sl.properties)
            else:
                print()
            sl.printSubLocations(prefix+"  ",False,inDepth=inDepth)
            if sl.getSubLocations():
                print()

            for o in sl.getObjects():
                print(prefix+" o> "+o.getDebugDescription())
