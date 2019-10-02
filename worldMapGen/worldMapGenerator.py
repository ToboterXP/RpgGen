from worldMapGen.world import *
from worldMapGen.locationTemplateMap import *
from locationGen.location import *
from locationGen.locationConnection import *
from locationGen.locationProperty import *
import randomUtil as ru
from util import Vector2

def generateWorldMap(coarseMap,fineMap,hydraulicMap,historyMap,locationTransform=Vector2(1000,1000),connectionCount=4):
    world = World(coarseMap,fineMap,hydraulicMap,historyMap)

    class ComboLoc:
        def __init__(self,historyLoc,worldLoc,type):
            self.historyLoc = historyLoc
            self.worldLoc = worldLoc
            self.type = type

    comboLocs = []

    for l in historyMap.getLocations():
        locType = LOCATION_TEMPLATE_MAP.get(l.getLocationType().name)
        if not locType:
            continue
        worldLoc = Location(locType.locationType,[],ru.getRandomSeed(),l.getPos()*locationTransform)
        worldLoc.attachProperty( LocationPropertyTemplate(ContextProperty, ("HistoryLocation",l)) )
        world.addLocation(worldLoc)
        comboLocs.append(ComboLoc(l,worldLoc,locType))

    #generate roads between locations
    civilizedLocs = []
    for c in comboLocs :
        if c.type.civilized:
            civilizedLocs.append(c)

    for l in civilizedLocs:
        connectCount = connectionCount - len(l.worldLoc.getConnections())
        if connectCount==0:
            continue
        closest = civilizedLocs[:connectCount]
        closest.sort(key=lambda c: abs(l.worldLoc.getPos()-c.worldLoc.getPos()), reverse=True)
        for a in civilizedLocs[connectCount:]:
            if a==l:
                continue
            if len(a.worldLoc.getConnections())>=connectionCount:
                continue
            i=0
            for c in closest:
                if abs(l.worldLoc.getPos()-c.worldLoc.getPos())>abs(l.worldLoc.getPos()-a.worldLoc.getPos()):
                    closest[i] = a
                    break
                i+=1

        for c in closest:
            LocationConnection(l.worldLoc,c.worldLoc)

    return world
