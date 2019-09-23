from locationGen.location import *
from locationGen.locationTypes.villageHouses import *
from locationGen.locationConnection import *
from util import *

from locationGen.locationType import *
from locationGen.locationContentTag import *
from locationGen.locationContentCollection import *
from locationGen.locationTypes.genericRooms import *
from locationGen.locationTypes.villageRoads import *

class TestRoomType(LocationType):
    def __init__(self):
        super().__init__([LEVEL_ROOM],
                        LocationContentCollection.EMPTY,
                        "TestRoom")

class TestVillageType(LocationType):
    def __init__(self):
        super().__init__([LEVEL_VILLAGE],
                        LocationContentCollection(
                            [
                                LocationContent(BasicHouseType())
                            ],
                            range(4,10),
                            (LEVEL_BUILDING,),
                            lambda subL,superC,superL: organizeWithRoads(subL,superC,superL,[VillageRoadType],[VillageRoadType],step=10)
                        ),"BasicVillage")

def test():
    testHouse = Location(TestVillageType(),[ LocationContent(TestRoomType()) ],0)
    testHouse2 = Location(TestVillageType(),[],0,Vector2(100,0))
    testHouse3 = Location(TestVillageType(),[],0,Vector2(-100,200))
    testConnection = LocationConnection(testHouse2,testHouse)
    testConnection = LocationConnection(testHouse3,testHouse)
    testHouse.loadContent()
    testHouse.printSubLocations()
    print("---Unloading and Reloading---\n\n\n")
    testHouse.unloadContent()
    testHouse.loadContent()
    testHouse.printSubLocations()

if __name__=="__main__":
    test()
