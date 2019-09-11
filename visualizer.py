import pygame as pg
from util import Vector2
from loader import GetLoadedObjectClass

pg.init()

def visualizeColorMap(mapGraph, picSize):
    mapSize = mapGraph.getMapSize()
    pict = pg.Surface((mapSize.a, mapSize.b))
    nodes = mapGraph.getNodes()

    for x in range(mapSize.a):
        for y in range(mapSize.b):
            mapPos = Vector2(x, y)
            pict.set_at((x,y), min(mapGraph.getNodes(), key=lambda n: abs(n.pos-mapPos)).getObject().getColor())

    pict = pg.transform.scale(pict,(picSize.a, picSize.b))

    return pict

def visualizeIconMap(mapGraph, iconPath, objectClass, picSize):
    mapSize = mapGraph.getMapSize()
    pict = pg.Surface((picSize.a, picSize.b))
    pict.fill((255,255,255))
    
    icons = {}
    for obj in GetLoadedObjectClass(objectClass):
        icons[obj.getName()] = pg.image.load(iconPath+"/"+obj.getName()+".png")
        icons[obj.getName()].set_colorkey((255,255,255))

    iconSize = tuple(icons.values())[0].get_size()
    
    for node in mapGraph.getNodes():
        imgPos = (node.getPos().a * picSize.a/mapSize.a-iconSize[0]/2, node.getPos().b * picSize.b/mapSize.b-iconSize[1]/2)

        pict.blit(icons[node.getObject().getName()], imgPos)

    return pict

class VisualGraph:
    def __init__(self, graph, color, radius=3, drawConnections=False, hydraulic=False):
        self.graph = graph
        self.color = color
        self.radius = radius
        self.drawConnections = drawConnections
        self.hydraulic = hydraulic


def visualizeGraph(mapGraphs, background, mapGraphScale, drawConnections=False):
    display = pg.display.set_mode(background.get_size(),0,0)

    mouseDown = False
    while True:
        display.blit(background,(0,0))
        for visualGraph in mapGraphs:
            mapGraph = visualGraph.graph
            for node in mapGraph.getNodes():
                radius = visualGraph.radius
                if visualGraph.hydraulic:
                    if node.stagnant:
                        radius = 5
                    else:
                        radius = min(round(node.getPower()/2), 4)
                
                pg.draw.circle(display, visualGraph.color, tuple((node.getPos()*mapGraphScale).round()), radius)

                if visualGraph.drawConnections:
                    for conn in node.connections:
                        pg.draw.line(display,visualGraph.color,tuple((node.getPos()*mapGraphScale).round()),tuple((conn.getPos()*mapGraphScale).round()))
                
        pg.display.flip()
        pg.event.pump()

        for event in pg.event.get(): 
            if event.type==pg.QUIT:
                pg.quit()
                return False

        if pg.mouse.get_pressed()[0]:
            if not mouseDown:
                for visGraph in mapGraphs:
                    mapGraph = visGraph.graph
                    mouseDown = True
                    mousePos=list(pg.mouse.get_pos())
                    if mapGraph.getMinDistance(Vector2(mousePos[0], mousePos[1])/mapGraphScale)< 10:
                        node = mapGraph.getClosest(Vector2(mousePos[0], mousePos[1])/mapGraphScale)
                        obj = node.getObject()
                        print("Name:",obj.name)
                        print("Position:", node.getPos())
                        print(obj.score)
                        for tag in obj.getTags():
                            print(tag.getName(),":",tag.getWeight())
                        print("-----------")
        else:
            mouseDown = False

        if pg.key.get_pressed()[pg.K_RETURN]:
            return True

        if pg.key.get_pressed()[pg.K_ESCAPE]:
            return True
                



    
