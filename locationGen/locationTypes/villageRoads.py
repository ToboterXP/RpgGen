from locationGen.locationType import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *
from locationGen.locationProperty import *

class VillageRoadType(LocationType):
    def __init__(self):
        super().__init__([VL_ROAD,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "VillageRoad",
                        propertyTemplates = [
                            BasicDescriptionPropertyTemplate(0,"A road")
                        ])
