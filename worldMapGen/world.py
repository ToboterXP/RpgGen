
class World:
    def __init__(self,coarseMap,fineMap,hydraulicMap,historyMap):
        self.coarseMap = coarseMap
        self.fineMap = fineMap
        self.hydraulicMap = hydraulicMap
        self.historyMap = historyMap
        self.locations = []

    def addLocation(self,loc):
        self.locations.append(loc)

    def getLocations(self):
        return self.locations
