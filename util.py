
import math
import random as r

class Vector2:
    def __init__(self,a,b):
        self.a = a
        self.b = b

    UNIT = None
    INVERT = None

    def __add__(self,other):
        return Vector2(self.a + other.a, self.b + other.b)

    def __sub__(self,other):
        return Vector2(self.a - other.a, self.b - other.b)

    def __mul__(self,other):
        return Vector2(self.a * other.a, self.b * other.b)

    def nMultiply(self,num):
        return Vector2(self.a * num, self.b * num)

    def nDivide(self,num):
        return Vector2(self.a / num, self.b / num)

    def __truediv__(self,other):
        return Vector2(self.a / other.a, self.b / other.b)

    def __abs__(self):
        return math.sqrt(self.a**2 + self.b**2)

    def __str__(self):
        return "{%.2f, %.2f}" % (round(self.a,2),round(self.b,2))

    def __iter__(self):
        return iter((self.a, self.b))

    def round(self):
        return Vector2(round(self.a), round(self.b))

    def random(bounds):
        return Vector2(r.random()*bounds.a,r.random()*bounds.b)

    def rotate(self, angle):
        radians = angle * 2*math.pi
        return Vector2(self.a*math.cos(radians) - self.b*math.sin(radians),
                       self.a*math.sin(radians) + self.b*math.cos(radians))

    def getAngleTowards(self,other):
        return math.acos( (self.a*other.a + self.b*other.b)/(abs(self)*abs(other)) ) / (2*math.pi)

    def floatMultiply(self, other):
        return Vector2(self.a * other, self.b * other)

    def __hash__(self):
        return int(self.a**20 + self.b)

    def __eq__(self,other):
        return self.a == other.a and self.b == other.b

    def normalize(self):
        return self.nDivide(abs(self))

Vector2.UNIT = Vector2(0,-1)
Vector2.INVERT = Vector2(-1,-1)

class MapGraph:
    def __init__(self, connectionDistance, size):
        self.nodes = []
        self.connectionDistance = connectionDistance
        self.mapSize = size
        self.cellularNodeMap = []
        for x in range(size.a//10+1):
            self.cellularNodeMap.append([])
            for y in range(size.b//10+1):
                self.cellularNodeMap[-1].append([])

    def getMapSize(self):
        return self.mapSize

    def getCellularPos(pos):
        return (pos/Vector2(10,10)).round()

    def addNode(self,node):
        cellPos = MapGraph.getCellularPos(node.getPos())
        self.cellularNodeMap[cellPos.a][cellPos.b].append(node)

        for n in self.getCloseNodes(node.getPos()):
            if abs(n.getPos() - node.getPos()) <= self.connectionDistance:
                n.addConnection(node)

        self.nodes.append(node)


    def getCloseNodes(self,pos,sort = None):
        cellPos = MapGraph.getCellularPos(pos)
        ret = []
        for x in range(cellPos.a-1,cellPos.a+2):
            for y in range(cellPos.b-1,cellPos.b+2):
                try:
                    ret += self.cellularNodeMap[x][y]
                except:
                    continue
        ret = ret if ret else self.getNodes()
        ret = list(filter(sort,ret))
        return ret

    def getMinDistance(self,pos,sort=None):
        if not self.getNodes():
            return 100000000
        return abs(min(self.getCloseNodes(pos,sort), key=lambda n: abs(n.getPos()-pos)).getPos()-pos)

    def getClosest(self,pos,sort=None):
        if not self.getNodes():
            return None
        return min(self.getCloseNodes(pos,sort), key=lambda n: abs(n.getPos()-pos))

    def getMultipleClosest(self,pos,num,sort=None):
        if not self.getNodes():
            return None
        nodes = self.getCloseNodes(pos,sort)
        if len(nodes)<num:
            nodes = list(filter(sort,self.getNodes()))
        nodes.sort(key=lambda n: abs(n.getPos()-pos))
        return nodes[:num]

    def removeNode(self,node):
        self.nodes.remove(node)
        node.destroy()
        cellPos = MapGraph.getCellularPos(node.getPos())
        self.cellularNodeMap[cellPos.a][cellPos.b].remove(node)
        del node

    def getNodes(self):
        return self.nodes



class MapGraphNode:
    def __init__(self,pos):
        self.setPos(pos)
        self.connections = []
        self.superConnections = []
        self.object = None
        self.attachedContext = {}

    def attachContext(self,context):
        self.attachedContext[context.__class__] = context

    def getAttachedContext(self,contextClass):
        return self.attachedContext[contextClass]

    def getPos(self):
        return self.pos

    def setPos(self,pos):
        self.pos = pos

    def setObject(self,o):
        self.object = o

    def getObject(self):
        return self.object

    def addConnection(self,other):
        if not other in self.connections:
            self.connections.append(other)
            other.addConnection(self)

    def removeConnection(self,other):
        self.connections.remove(other)

    def addSuperConnection(self,conn):
        self.superConnections.append(conn)

    def getSuperConnections(self):
        return self.superConnections

    def hasConnections(self):
        return bool(self.connections)

    def getConnections(self):
        return self.connections

    def destroy(self):
        for conn in self.connections:
            conn.removeConnection(self)

    def getCollectiveTags(self):
        tags = self.getObject().getTags()[:]
        for supObj in self.getSuperConnections():
            for tag in supObj.getCollectiveTags():
                tags.append(tag*0.7)

        return tags




class Tag:
    def __init__(self,name,parents=tuple(),excluded=tuple(),valueRange = (0,1)):
        self.name = name
        self.parents = tuple(parents)
        self.valueRange = valueRange
        self.compareVals = {}
        self.excluded = excluded

    def getValueRange(self):
        return self.valueRange

    def getName(self):
        return self.name

    def getParents(self):
        return self.parents

    def getWeight(self):
        return 1

    def getTag(self):
        return self

    def compare(self,other,i=0):
        if self.getName()==other.getName():
            return 1

        if other.getName() in self.compareVals.keys():
            return self.compareVals[other.getName()]

        score = 0
        amount = 0
        for myTag in self.getParents()+(self,):
            for otherTag in other.getParents()+(other,):
                if myTag==self and otherTag==other:
                    continue
                score += myTag.compare(otherTag,i+1)
                amount += 1

        if amount==0:
            self.compareVals[other.getName()] = 0
            return 0


        self.compareVals[other.getName()] = score/amount
        return score/amount

class WeightedTag:
    def __init__(self,tag,weight):
        self.tag = tag
        self.weight = weight

    def getName(self):
        return self.getTag().getName()

    def getParents(self):
        return self.getTag().getParents()

    def getTag(self):
        return self.tag

    def getWeight(self):
        return self.weight

    def __mul__(self,other):
        return WeightedTag(self.tag, self.weight*other)

    def compare(self,other,i=0):
        weight = max(self.getWeight(),other.getWeight())-abs(self.getWeight()-other.getWeight())
        return max(self.getTag().compare(other.getTag(),i+1)*weight, 0)


class TaggedObjectTemplate:
    def __init__(self, name, weightedTags, color, baseChance):
        self.name = name
        self.color = color
        self.baseChance = baseChance
        self.weightedTags = weightedTags #2D - First D list of tags, Second D possible tags

    def getName(self):
        return self.name

    def instantiate(self):
        tagList = []

        for tagPoss in self.weightedTags:
            tagList.append(r.choice(tagPoss))

        return TaggedObject(self.name, tagList, self.color, self, self.baseChance)


class TaggedObject:
    def __init__(self,name,weightedTags,color,template,baseChance):
        self.name = name
        self.weightedTags = weightedTags
        self.color = color
        self.score = -1
        self.template = template
        self.baseChance = baseChance

    def getName(self):
        return self.name

    def getTemplate(self):
        return self.template

    def getColor(self):
        return self.color

    def getTags(self):
        return self.weightedTags

    def addTag(self,wtag):
        self.weightedTags.append(wtag)

    def compare(self,other):
        score = 0
        amount = 0
        for myTag in self.getTags():
            for otherTag in other.getTags():
                score += myTag.compare(otherTag)
                amount += myTag.getWeight() * otherTag.getWeight()

        return score/amount*self.baseChance
