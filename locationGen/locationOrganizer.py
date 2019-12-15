
import math
import randomUtil as r
import randomUtil as ru
from locationGen.locationConnection import LocationConnection
from locationGen.locationContent import *
from util import *
import copy
from locationGen.locationType import *

def organizeBasic(subLocations,superConnections,superLocation,extraConRate=0.3,step = Vector2(1,1)):
    if not subLocations:
        return
    assert superConnections
    organizedLocs = copy.copy(subLocations)
    organizedPos = {}
    revOrganizedPos = {}
    side = math.ceil(math.sqrt(len(subLocations)))
    r.shuffle(organizedLocs)
    i = 0
    maxX = 0
    maxY = 0
    origin = superLocation.getPos() - step.nMultiply(side/2)
    for x in range(side):
        for y in range(side):
            organizedPos[organizedLocs[i]] = Vector2(x,y)
            revOrganizedPos[Vector2(x,y)] = organizedLocs[i]
            organizedLocs[i].setPos(origin + step*Vector2(x,y))
            i+=1
            if i==len(organizedLocs):
                maxY = y
                break
        if i==len(organizedLocs):
            maxX = x
            break

    unconnected = organizedLocs
    connected = []

    startedConnection = False
    for sc in superConnections[:]:
        direction = sc.getDirection(superLocation)
        selectedLoc = None
        if abs(direction.a)<abs(direction.b):
            x = r.randint(0,maxX//2)
            if direction.a>0:
                x+=maxX//2
            y = 0 if direction.b<0 else maxX
            selectedLoc = revOrganizedPos[Vector2(x,y)]
        else:
            y = r.randint(0,maxY//2)
            if direction.b>0:
                y+=maxY//2
            x = 0 if direction.a<0 else maxX
            selectedLoc = revOrganizedPos[Vector2(x,y)]

        LocationConnection(selectedLoc,superLocation,l2c=sc)
        if not startedConnection:
            startedConnection = True
            connected.append(selectedLoc)
            unconnected.remove(selectedLoc)

    while unconnected:
        if len(connected) < len(unconnected):
            for con in connected:
                dirs = [Vector2(1,0),Vector2(0,1),Vector2(-1,0),Vector2(0,-1)]
                r.shuffle(dirs)
                for d in dirs:
                    targetPos = organizedPos[con]+d
                    target = revOrganizedPos.get(targetPos)
                    if not target:
                        continue
                    if target in unconnected:
                        newConnection = LocationConnection(con,target)
                        unconnected.remove(target)
                        connected.append(target)
                        break
        else:
            for con in unconnected:
                dirs = [Vector2(1,0),Vector2(0,1),Vector2(-1,0),Vector2(0,-1)]
                r.shuffle(dirs)
                for d in dirs:
                    targetPos = organizedPos[con]+d
                    target = revOrganizedPos.get(targetPos)
                    if not target:
                        continue
                    if target in connected:
                        newConnection = LocationConnection(con,target)
                        unconnected.remove(con)
                        connected.append(con)
                        break

    cCount = round(extraConRate*len(subLocations)*(r.random()+0.3))
    for i in range(cCount*10):
        loc = r.choice(subLocations)
        d = r.choice((Vector2(1,0),Vector2(0,1),Vector2(-1,0),Vector2(0,-1)))
        otherLoc = revOrganizedPos.get(organizedPos[loc]+d)
        if not otherLoc:
            continue
        duplicate = False
        for con in loc.getConnections():
            if con.getOther(loc) == otherLoc:
                duplicate = True
                break
        if duplicate:
            continue

        newConnection = LocationConnection(loc,otherLoc)

        cCount -= 1
        if cCount <=0:
            break



def organizeWithRoads(subLocations,superConnections,superLocation,roadTypes,crossingTypes,step = 1):
    externalRoadCount = len(superConnections)
    locsPerExRoad = math.ceil(len(subLocations)/externalRoadCount)
    centralCrossing = LocationContent(r.choice(crossingTypes)).getLocation([],ru.getRandomSeed(),superLocation)
    centralCrossing.setPos(superLocation.getPos())

    remainingLocations = subLocations[:]
    subLocations.append(centralCrossing)
    for exit in superConnections[:]:
        assignedLocations = remainingLocations[:locsPerExRoad] if len(remainingLocations)>=locsPerExRoad else remainingLocations[:]
        for l in assignedLocations:
            remainingLocations.remove(l)
        print(exit.l1.isTopLocation(),exit.l2.isTopLocation(),exit.l1.getPos(),exit.l2.getPos())
        roadDirection = exit.getDirection(superLocation).normalize().nMultiply(step)
        lastRoad = centralCrossing
        roadPos = centralCrossing.getPos()
        while assignedLocations:
            roadPos += roadDirection
            newRoad = LocationContent(r.choice(roadTypes)).getLocation([],ru.getRandomSeed(),superLocation)
            newRoad.setPos(roadPos)
            roadConnection = LocationConnection(newRoad,lastRoad)
            subLocations.append(newRoad)
            lastRoad = newRoad

            leftPos = roadPos+roadDirection.rotate(0.25)
            leftLoc = assignedLocations.pop()
            leftLoc.setPos(leftPos)
            LocationConnection(newRoad,leftLoc)

            if not assignedLocations:
                break

            rightPos = roadPos+roadDirection.rotate(0.75)
            rightLoc = assignedLocations.pop()
            rightLoc.setPos(rightPos)
            LocationConnection(newRoad,rightLoc)

        LocationConnection(superLocation,lastRoad,l1c=exit)

    assert not remainingLocations
