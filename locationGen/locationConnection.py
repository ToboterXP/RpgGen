from util import Vector2

class LocationConnection:
    def __init__(self,l1,l2,l1c=None,l2c=None):
        self.l1 = l1
        l1.addConnection(self)
        self.l1Connection = l1c
        if l1c:
            l1c.setLocationConnection(l1,self)
        self.l2 = l2
        l2.addConnection(self)
        self.l2Connection = l2c
        if l2c:
            l2c.setLocationConnection(l2,self)

    def setLocationConnection(self,loc,conn):
        if loc == self.l1:
            self.l1Connection = conn
        else:
            self.l2Connection = conn

    def delete(self):
        self.l1.removeConnection(self)
        self.l2.removeConnection(self)
        if self.l1Connection:
            self.l1Connection.setLocationConnection(self.l1,None)
        if self.l2Connection:
            self.l2Connection.setLocationConnection(self.l2,None)

    def isConnection(self):
        return True

    def getDirection(self,start):
        pos1 = self.l1.getPos()
        pos2 = self.l2.getPos()
        if start==self.l2:
            t = pos1
            pos1 = pos2
            pos2 = t

        return pos2-pos1

    def getOther(self,l):
        return self.l1 if l==self.l2 else self.l2

    def getLocationConnection(self,l):
        return self.l1Connection if l==self.l1 else self.l2Connection

    def getConnectionStart(self):
        if self.l1c:
            return self.l1c.getConnectionStart()
        else:
            return self.l1

    def getConnectionEnd(self):
        if self.l2c:
            return self.l2c.getConnectionStart()
        else:
            return self.l2

    def getSimplifiedConnection(self):
        return LocationConnection(self.getConnectionStart(), self.getConnectionEnd())
