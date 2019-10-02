from locationGen.locationType import *
from locationGen.locationContentTag import *
from locationGen.locationContent import *
from locationGen.locationContentCollection import *
from locationGen.locationTypes.genericRooms import *
from locationGen.locationTypes.villageRoads import *
from locationGen.locationTypes.villageHouses import *

BasicVillageType = LocationType([LEVEL_VILLAGE],
                        LocationContentCollection(
                            [
                                LocationContent(BasicHouseType)
                            ],
                            range(4,10),
                            (LEVEL_BUILDING,),
                            lambda subL,superC,superL: organizeWithRoads(subL,superC,superL,[VillageRoadType],[VillageRoadType],step=10)
                        ),"BasicVillage")
