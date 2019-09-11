
from util import *
from loader import *

import random as r

class HydraulicNode(MapGraphNode):
    def __init__(self,pos,power,score, direction = None, isSource=False):
        super().__init__(pos)
        self.power = power
        self.basePower = power
        self.stagnant = False
        self.streamInputs = []
        self.streamOutputs = []
        self.direction = direction
        self.score = 0
        self.length = 0
        self.isSource = isSource

    def getStreamOutputs(self):
        return self.streamOutputs

    def addStreamOutput(self,out,end=False):
        self.streamOutputs.append(out)
        if not end:
            out.addStreamInput(self,True)

    def getStreamInputs(self):
        return self.streamInputs

    def getParents(self):
        ret = self.streamInputs[:]
        for stream in self.streamInputs:
            ret += stream.getParents()

        return ret

    def addStreamInput(self,inp,end=False):
        if self.isSource:
            self.isSource = False
            self.addPower(-self.basePower)
        self.addPower(inp.getPower())
        if inp.length+1>self.length:
            self.length = inp.length+1
        self.streamInputs.append(inp)
        
        if not end:
            inp.addStreamOutput(self,True)

    def getPower(self):
        return self.power

    def addPower(self,change):
        self.power += change
        for out in self.getStreamOutputs():
            out.addPower(change)

    def getDirection(self):
        return self.direction

    def setDirection(self,direction):
        self.direction = direction

    def generateMapGraphData(self,hydraulicObjects):

        if self.stagnant:
            if self.power<=3:
                self.setObject(hydraulicObjects["Pond"].instantiate())
            else:
                self.setObject(hydraulicObjects["Lake"].instantiate())             
        else:
            if self.power<=3:
                self.setObject(hydraulicObjects["Stream"].instantiate())
            else:
                self.setObject(hydraulicObjects["River"].instantiate())

        self.getObject().score = self.power
        for node in self.getStreamOutputs():
            node.addConnection(self)


def evaluateRiverTarget(fineBiome):
    score = 0
    for tag in fineBiome.getCollectiveTags():
        if tag.getName()=="mountainous":
            score += tag.getWeight()*1.5
        if tag.getName()=="hilly":
            score += tag.getWeight()
        if tag.getName()=="water":
            score -= tag.getWeight()
        if tag.getName()=="flat":
            score -= tag.getWeight()*0.5

    return score
        

def generateHydraulicMap(mapSize, fineBiomes, sourceCellSize, sourceChance, iterationCount, smallStepLength, largeStepLength, mergeDistance):
    fineBiomeNodes = fineBiomes.getNodes()

    hydroGraph = MapGraph(0,mapSize)

    streamsInProcess = []

    #generate stream sources
    usedFineBiomes = []
    
    for x in range(sourceCellSize.a//2, mapSize.a, sourceCellSize.a):
        for y in range(sourceCellSize.b//2, mapSize.b, sourceCellSize.b):
            if r.random()<sourceChance:
                source = fineBiomes.getClosest(Vector2(x,y))
                
                if source in usedFineBiomes:
                    continue
                
                tags = source.getCollectiveTags()
                acceptable = False
                for tag in tags:
                    if tag.getName()=="mountainous" and tag.getWeight()>=1:
                        acceptable = True
                        break
                    if tag.getName()=="hilly" and tag.getWeight()>=0.5:
                        acceptable = True
                        break
                    if tag.getName()=="forested" and tag.getWeight()>=1:
                        acceptable = True
                        break
                    
                if not acceptable:
                    continue
                
                usedFineBiomes.append(source)
                streamsInProcess.append(HydraulicNode(source.getPos(),1, evaluateRiverTarget(source), isSource=True))

    #iterate stream extension

    for i in range(iterationCount):
        
        newStreams = []

        for stream in streamsInProcess:

            #try twice, once with large step, once with small step
            stepLength = smallStepLength
            for j in range(2):
                #ignore streams outside map
                posDiff = mapSize - stream.getPos()
                if posDiff.a<0 or posDiff.b<0 or posDiff.a>mapSize.a or posDiff.b>mapSize.b:
                    break

                #assign direction if not present
                if not stream.getDirection():
                    angles = []
                    angle = 0
                    while angle<1:
                        angles.append(angle)
                        angle+=0.1

                    r.shuffle(angles)
                    minScore = 1000
                    for angle in angles:
                        direction = Vector2.UNIT.rotate(angle).floatMultiply(stepLength)
                        pos = direction + stream.pos
                        score = evaluateRiverTarget(fineBiomes.getClosest(pos))
                        if score<stream.score and score<minScore :
                            stream.setDirection(direction)
                            minScore = score

                #generate possible next positions
                possiblePos = []

                angleStep = 0.02
                angleRange = 0.2

                angle = -angleRange
                while angle <=angleRange:
                    possAngle = angle + r.random()*angleStep

                    possPos = Vector2.UNIT.rotate(possAngle).floatMultiply(stepLength) + stream.getPos()

                    possiblePos.append(possPos)
                    angle += angleStep

                streamParents = stream.getParents()
                riverScore = {}
                for pos in possiblePos:
                    closest = fineBiomes.getClosest(pos)
                    riverScore[pos] = evaluateRiverTarget(closest)*(0.8+r.random()*0.4)
                    if closest in usedFineBiomes:
                        riverScore[pos] = 100

                #get highest scoring positions
                targetPos = max( possiblePos,key= lambda pos: stream.score-riverScore[pos] )

                #merge streams if close enough
                closestStream = hydroGraph.getClosest(targetPos)
                if closestStream:
                    closestDist = abs(closestStream.getPos() - targetPos)
                    for nstream in newStreams:
                        if abs(nstream.getPos() - targetPos) < closestDist:
                            closestStream = nstream
                            closestDist = abs(nstream.getPos() - targetPos)

                if (not closestStream in streamParents) and closestStream and (
                    abs(closestStream.getPos() - targetPos) < mergeDistance if not closestStream.stagnant else mergeDistance * max(1,min(1.7,1.7*closestStream.getPower()/5))):
                    
                    closestStream.addStreamInput(stream)
                    break

                #maybe set stream as stagnant if difference isn't large enough
##                if (stream.score-riverScore[pos])<r.random()*0.2-0.3 and (stream.length-2)%5==0 and r.random()<0.7:
##                    stream.stagnant = True

                if (stream.score-riverScore[pos])<r.random()*0.2-0.4 and stream.length>r.randint(3,8):
                    if j==0:
                        stepLength = largeStepLength
                        continue
                    else:
                        stream.stagnant = True
                        break

                #create next node
                newStream = HydraulicNode(targetPos, 0.05, riverScore[pos], targetPos-stream.getPos() )
                stream.addStreamOutput(newStream)
                newStreams.append(newStream)
                usedFineBiomes.append(fineBiomes.getClosest(targetPos))
                break
            
        for stream in streamsInProcess:
            hydroGraph.addNode(stream)
        streamsInProcess = newStreams


    #generate map graph data
    hydraulicObjects = {}
    for hydroObj in GetLoadedObjectClass("hydraulics"):
        hydraulicObjects[hydroObj.getName()] = hydroObj
        
    for node in hydroGraph.getNodes():
        node.generateMapGraphData(hydraulicObjects)
        

    return hydroGraph
            

            

                

            
        

    
    
