from locationGen.locationType import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *
from locationGen.locationProperty import *

VillageRoadType = LocationType([VL_ROAD,LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "VillageRoad",
                        propertyTemplates = [
                            LocationPropertyTemplate(BasicDescriptionProperty,(0,"A road","road"))
                        ])
