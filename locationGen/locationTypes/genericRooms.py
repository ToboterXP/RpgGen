from locationGen.locationType import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *
from locationGen.locationProperty import *
from locationGen.objects.lootTables.village.basicFurniture import *

LivingRoomType = LocationType([RO_GEN_LIVING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "LivingRoom",
                        propertyTemplates = [
                            LocationPropertyTemplate(BasicDescriptionProperty,(0,"A [nice|cozy|small] living room","living room")),
                            LocationPropertyTemplate(RandomObjectsProperty, (VILLAGE_BASIC_FURNITURE,4,0.3))
                        ])


BedRoomType = LocationType([RO_GEN_SLEEPING_QUARTER,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "BedRoom",
                        propertyTemplates = [
                            LocationPropertyTemplate(BasicDescriptionProperty,(0,"A [nice|cozy|small] bed room","bed room")),
                            LocationPropertyTemplate(RandomObjectsProperty, (VILLAGE_BASIC_FURNITURE,3,0.3))
                        ])
