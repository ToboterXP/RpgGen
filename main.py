
from loader import *
from util import *
from visualizer import *
from mapGenerator import *
from hydraulicMapGenerator import *
from historyGen.historyMapGenerator import *
import random
import sys



def generateWorld(menu=True):
    print("Loading Files")
    with open("./tags/nature/coarseBiomes.txt","r") as f:
        LoadObjectFile(f,"coarseBiomes")

    with open("./tags/nature/fineBiomes.txt","r") as f:
        LoadObjectFile(f,"fineBiomes")

    with open("./tags/nature/hydraulics.txt","r") as f:
        LoadObjectFile(f,"hydraulics")

    with open("./tags/civilization/races.txt","r") as f:
        LoadObjectFile(f,"races")

    with open("./tags/civilization/civilLocations.txt","r") as f:
        LoadObjectFile(f,"civilLocations")

    with open("./tags/civilization/generalLocations.txt","r") as f:
        LoadObjectFile(f,"generalLocations")

    print("Loaded files:",LOADED_OBJECTS.keys())

    MAP_SIZE = Vector2(150,150)
    WINDOW_SIZE = Vector2(750,750)
    HISTORY_LENGTH = 100
    DISPLAY_HISTORY = True

    print("Generating coarse map")    
    coarseBiomeMap = generateEmptyMap(MAP_SIZE,Vector2(4,4), Vector2(15,15), 28)
    fillMap(coarseBiomeMap, "coarseBiomes")

    print("Generating fine map")
    fineBiomeMap = generateEmptyMap(MAP_SIZE,Vector2(2,2), Vector2(7,7), 14)
    generateSuperConnections(fineBiomeMap, coarseBiomeMap, 28, 2)
    fillMap(fineBiomeMap, "fineBiomes", superInfluence=3)

    print("Generating hydraulic map")
    hydroMap = generateHydraulicMap(MAP_SIZE, fineBiomeMap, Vector2(15,15),0.6, 60, 4,4, 4)

    print("Generating racial distribution")
    racialMap = generateEmptyMap(MAP_SIZE, Vector2(4,4), Vector2(15,15), 28)
    generateSuperConnections(racialMap, coarseBiomeMap, 28, 1)
    fillMap(racialMap, "races", superInfluence=3)

    print("Generating civil locations")
    civilLocMap = generateEmptyMap(MAP_SIZE, Vector2(3,3), Vector2(10,10),20)
    generateSuperConnections(civilLocMap, racialMap, 28, 1)
    generateSuperConnections(civilLocMap, fineBiomeMap, 28, 1)
    generateSuperConnections(civilLocMap, hydroMap, 8, 1)
    fillMap(civilLocMap, "civilLocations", superInfluence = 3, nothingThreshold = 0.2)

    print("Generating general locations")
    generalLocMap = generateEmptyMap(MAP_SIZE, Vector2(2,2), Vector2(7,7),14)
    generateSuperConnections(generalLocMap, civilLocMap, 8, 3)
    generateSuperConnections(generalLocMap, fineBiomeMap, 28, 1)
    generateSuperConnections(generalLocMap, racialMap, 28, 2)
    fillMap(generalLocMap, "generalLocations", superInfluence = 3, nothingThreshold = 0)

    print("Generating history")
    historyMap = generateHistory(fineBiomeMap, racialMap, civilLocMap, generalLocMap, HISTORY_LENGTH, Vector2(25,25),2)

    print("Displaying history menu")
    if not menu:
        return
    if DISPLAY_HISTORY:
        displayHistoryExplorer(historyMap, HISTORY_LENGTH)
        return False

    print("Generating coarse BG")
    coarseBG = visualizeColorMap(coarseBiomeMap, WINDOW_SIZE)

    print("Generating fine BG")
    fineBG = visualizeIconMap(fineBiomeMap, "./tags/nature/fineBiomeIcons", "fineBiomes", WINDOW_SIZE)
    fineBG.set_colorkey((255,255,255))
    coarseBG.blit(fineBG, (0,0))

    print("Generating race BG")
    raceBG = visualizeIconMap(racialMap, "./tags/civilization/racialIcons", "races", WINDOW_SIZE)
    raceBG.set_colorkey((255,255,255))
    coarseBG.blit(raceBG, (0,0))

    print("Generating civil location BG")
    civilLocBG = visualizeIconMap(civilLocMap, "./tags/civilization/civilLocationIcons", "civilLocations", WINDOW_SIZE)
    civilLocBG.set_colorkey((255,255,255))
    coarseBG.blit(civilLocBG, (0,0))

    print("Generating general location BG")
    civilLocBG = visualizeIconMap(generalLocMap, "./tags/civilization/civilLocationIcons", "generalLocations", WINDOW_SIZE)
    civilLocBG.set_colorkey((255,255,255))
    coarseBG.blit(civilLocBG, (0,0))
    
    print("Visualizing")
    return visualizeGraph(
        #[VisualGraph(fineBiomeMap,(0,0,0)), VisualGraph(coarseBiomeMap,(255,255,0)), VisualGraph(racialMap,(0,0,255))
                    #, VisualGraph(civilLocMap,(255,0,0))]
                    [VisualGraph(hydroMap,(0,0,255),drawConnections=True,hydraulic=True)]
                   , coarseBG, WINDOW_SIZE/MAP_SIZE, False)


if __name__=="__main__":
    sys.setrecursionlimit(100)
##    for i in range(4,100):
##        r.seed(i)
##        try:
##            generateWorld(False)
##        except:
##            print(i)
##            print("-----")
##            exit()
    r.seed(10)
    run = True
    while run:
        run = generateWorld()
