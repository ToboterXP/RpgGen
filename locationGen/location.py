import random as r
import copy
from util import *

class Location:
    def __init__(self,type,given,seed,pos=Vector2(0,0)):
        self.seed = seed
        self.pos = pos
        self.type = type
        self.given = given
        self.taken = []
        self.subLocations = []
        self.connections = []

    def getPos(self):
        return self.pos

    def setPos(self,pos):
        self.pos = pos

    def isConnection(self):
        return False

    def addConnection(self,conn):
        self.connections.append(conn)

    def getConnections(self):
        return self.connections

    def getSubLocations(self):
        return self.subLocations

    def getType(self):
        return self.type

    def loadContent(self):
        r.seed(self.seed)
        self.subLocations = self.type.rootContentCollection.generateLocations(self.given,self.taken,self.connections,self)
        for loc in self.subLocations:
            loc.loadContent()

    def unloadContent(self,deleteConns=False):
        for sl in self.subLocations:
            sl.unloadContent(True)
            del sl
        if deleteConns:
            for c in self.connections:
                c.delete()
        self.given += self.taken
        self.taken = []
        self.subLocations = []

    def printSubLocations(self,prefix="",start=True):
        if start:
            print(self.type.name)
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
            print(prefix+str(i)+".", sl.getType().name ,connections,sl.getPos())
            sl.printSubLocations(prefix+"  ",False)
            if sl.getSubLocations():
                print()