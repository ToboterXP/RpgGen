from locationGen.locationType import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *

class LivingRoomType(LocationType):
    def __init__(self):
        super().__init__([RO_GEN_LIVING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "LivingRoom")


class BedRoomType(LocationType):
    def __init__(self):
        super().__init__([RO_GEN_SLEEPING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "BedRoom")
