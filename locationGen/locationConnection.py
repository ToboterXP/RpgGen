from util import Vector2

class LocationConnection:
    def __init__(self,l1,l2,l1c=None,l2c=None,dummy=False):
        self.l1 = l1

        if not dummy:
            l1.addConnection(self)

        self.l1Connection = l1c
        if l1c and not dummy:
            l1c.setLocationConnection(l1,self)
        self.l2 = l2

        if not dummy:
            l2.addConnection(self)
        self.l2Connection = l2c
        if l2c and not dummy:
            l2c.setLocationConnection(l2,self)

    def setLocationConnection(self,loc,conn):
        if loc == self.l1:
            self.l1Connection = conn
        else:
            self.l2Connection = conn

    def connectsTopLocation(self):
        return self.l1.isTopLocation() and self.l2.isTopLocation()

    def containsTopLocation(self,alreadyHandled=None,):
        if not alreadyHandled:
            alreadyHandled = []

        if not self.l1 in alreadyHandled:
            alreadyHandled.append(self.l1)
            if self.l1.isTopLocation():
                return True
            if self.l1Connection:
                return self.l1Connection.containsTopLocation(alreadyHandled)

        if not self.l2 in alreadyHandled:
            alreadyHandled.append(self.l2)
            if self.l2.isTopLocation():
                return True
            if self.l2Connection:
                return self.l2Connection.containsTopLocation(alreadyHandled)

        return False



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

    def getOtherConnection(self,l):
        return self.l1Connection if l==self.l2 else self.l2Connection

    def getLocationConnection(self,l):
        return self.l1Connection if l==self.l1 else self.l2Connection

    def getConnectionInDir(self,other=None):
        c = self.getOtherConnection(other)
        if not c:
            return self.getOther(other)
        else:
            return c.getConnectionInDir(self.getOther(other))

    def getSimplifiedConnection(self):
        return LocationConnection(self.getConnectionInDir(self.l1), self.getConnectionInDir(self.l2), dummy=True)
