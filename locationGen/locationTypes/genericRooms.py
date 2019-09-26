from locationGen.locationType import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *
from locationGen.locationProperty import *
from locationGen.objects.lootTables.village.basicFurniture import *

class LivingRoomType(LocationType):
    def __init__(self):
        super().__init__([RO_GEN_LIVING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "LivingRoom",
                        propertyTemplates = [
                            BasicDescriptionPropertyTemplate(0,"A [nice|cozy|small] living room"),
                            LocationPropertyTemplate(RandomObjectsProperty, (VILLAGE_BASIC_FURNITURE,4,0.3))
                        ])


class BedRoomType(LocationType):
    def __init__(self):
        super().__init__([RO_GEN_SLEEPING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "BedRoom",
                        propertyTemplates = [
                            BasicDescriptionPropertyTemplate(0,"A [nice|cozy|small] bed room"),
                            LocationPropertyTemplate(RandomObjectsProperty, (VILLAGE_BASIC_FURNITURE,3,0.3))
                        ])
