from locationGen.locationType import *
from locationGen.locationContent import *
from locationGen.locationContentCollection import *
from locationGen.location import Location
from locationGen.locationContentTag import *
from locationGen.locationTypes.genericRooms import *
from locationGen.locationOrganizer import *

class BasicHouseType(LocationType):
    def __init__(self):
        super().__init__([VL_BUILDING,LEVEL_BUILDING],
                        LocationContentCollection(
                            [
                                LocationContent(LivingRoomType()),
                                LocationContent(BedRoomType())
                            ],
                            range(2,5),
                            (LEVEL_ROOM,),
                            lambda subL,superC,superL: organizeBasic(subL,superC,superL,step=Vector2(1,1))
                        ),"BasicHouse")
