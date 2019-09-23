from locationGen.locationType import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *
from locationGen.locationProperty import *

class LivingRoomType(LocationType):
    def __init__(self):
        super().__init__([RO_GEN_LIVING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "LivingRoom",
                        propertyTemplates = [
                            BasicDescriptionPropertyTemplate(0,"A [nice|cozy|small] living room")
                        ])


class BedRoomType(LocationType):
    def __init__(self):
        super().__init__([RO_GEN_SLEEPING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "BedRoom",
                        propertyTemplates = [
                            BasicDescriptionPropertyTemplate(0,"A [nice|cozy|small] bed room")
                        ])
