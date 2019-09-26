
from loader import *
from util import *
from visualizer import *

import randomUtil as r


def generateEmptyMap(dimensions,quadrantBounds, quadrantSize, connectionDistance):
    mapGraph = MapGraph(connectionDistance, dimensions)

    for x in range(0,dimensions.a,quadrantSize.a):
        for y in range(0, dimensions.b, quadrantSize.b):
            mapGraph.addNode( MapGraphNode(Vector2(x,y)+Vector2.random(quadrantSize-quadrantBounds)) )

    return mapGraph

def generateSuperConnections(mapGraph,superGraph,connectionDistance,maxSuperNodes):
    for node in mapGraph.getNodes():
        superConnections = superGraph.getNodes()[:]
        superConnections.sort(key = lambda n:abs(node.pos - n.pos))
        for conn in superConnections[:maxSuperNodes]:
            if abs(node.pos - conn.pos) <= connectionDistance:
                node.addSuperConnection(conn)
                              
    

def fillMap(mapGraph, objectClass, superInfluence=1, nothingThreshold=0):
    templates = GetLoadedObjectClass(objectClass)

    objectSuggestions = []
    for template in templates+templates:
        objectSuggestions.append(template.instantiate())

    nodesToRemove = []
    for node in mapGraph.getNodes():
        r.shuffle(objectSuggestions)
        
        scoredSuggs = {}
        for obj in objectSuggestions:
            score = 0
            connCount = 0
            for conn in node.getConnections():
                if conn.getObject():
                    score += obj.compare(conn.getObject()) / abs(node.getPos()-conn.getPos())
                    connCount+=1

            superScore = 0
            for superConn in node.getSuperConnections():
                superScore += obj.compare(superConn.getObject())
            
            finalScore = 0
            if connCount>0:
                finalScore += score/connCount

            if node.getSuperConnections():    
                finalScore += superScore/len(node.getSuperConnections())*superInfluence

            scoredSuggs[obj] = finalScore
            obj.score = finalScore

        order = objectSuggestions[:]
        order.sort(key = lambda obj: scoredSuggs[obj])
        order = order[2*len(order)//3:]
        for obj in objectSuggestions:
            if not obj in order:
                scoredSuggs.pop(obj)
        
            
        targetVal = r.random()*sum(scoredSuggs.values())
        usedObject = r.choice(order)
        for obj in order:
            targetVal -= scoredSuggs[obj]
            if targetVal <= 0:
                usedObject = obj
                break
        

        objectSuggestions = []
        for template in templates+templates:
            objectSuggestions.append(template.instantiate())

        if scoredSuggs[obj] < nothingThreshold:
            nodesToRemove.append(node)
        else:
            node.setObject(usedObject)

    for node in nodesToRemove:
        mapGraph.removeNode(node)
        
if __name__=="__main__":
    pass

    

    
    
    
    
