from locationGen.objects.objectProperty import *
import randomUtil as r

class LocationObject:
    def __init__(self,location,propertyTemplates):
        self.location = location
        if location:
            location.addObject(self)
        self.properties = [pt.instantiate(self) for pt in propertyTemplates]
        for p in self.getProperties(ObjectPropertyType.OPT_INIT):
            r.pushSeed(r.getRandomSeed())
            p.onInit()
            r.popSeed()

    def getLocation(self):
        return self.location

    def move(self,location):
        self.location.removeObject(self)
        location.addObject(self)
        self.location = location

    def delete(self):
        self.location.removeObject(self)

    def getProperty(self,type):
        for p in self.properties:
            if type in p.getTypes():
                return p
        return None

    def getDebugDescription(self):
        ret = self.getProperty(ObjectPropertyType.OPT_DESCRIPTION).getName() + " ("
        for c in self.getProperties(ObjectPropertyType.OPT_CONTAINER):
            for i in c.getItems():
                ret += i.getDebugDescription()+", "
        return ret+")"

    def getProperties(self,type):
        for p in self.properties:
            if type in p.getTypes():
                yield p
