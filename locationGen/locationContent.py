from locationGen.location import Location

class LocationContent:
    def __init__(self,type):
        self.type = type

    def getAttachTags(self):
        return self.type.attachTags

    def getTags(self):
        return self.type.tags

    def getItems(self):
        return []

    def getLocation(self,given,seed,superLocation):
        return Location(self.type,given,seed, superLocation,propertyTemplates=self.type.propertyTemplates)
