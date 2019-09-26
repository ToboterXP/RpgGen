from historyGen.historyEventList import *
from historyGen.historyEvents import *
from historyGen.historyLocations import *
from util import *
from graphicMenus import *
import randomUtil as r
import math


def generateHistory(fineMap,racialMap, civilLocMap, generalLocMap, historyLen, eventCellSize, maxCellEvents):

    unprocessedEvents = []
    historyMap = HistoryMap( fineMap.getMapSize())
    context = HistoricMapContext(fineMap, racialMap ,civilLocMap, generalLocMap, historyMap)

    locCount = {}
    for civilLoc in civilLocMap.getNodes()+generalLocMap.getNodes():
        name = civilLoc.getObject().getName()+str(locCount.setdefault(civilLoc.getObject().getName(),0))
        histLoc = HistoryLocation(civilLoc,context,r.random()<0.3, name)
        historyMap.addLocation(histLoc)
        locCount[civilLoc.getObject().getName()] += 1

    for year in range(historyLen):
        cCount = 0
        for c in historyMap.getCharacters():
            if c.getCurrentState().alive:
                cCount += 1
                
        for x in range(round((fineMap.getMapSize()/eventCellSize).a)):
            for y in range(round((fineMap.getMapSize()/eventCellSize).b)):
                pos = Vector2.random(eventCellSize) + Vector2(x,y)*eventCellSize
                eventCount = r.randint(0, min(maxCellEvents, math.ceil(maxCellEvents*(cCount/200)+0.01)) )
                i=0
                while i<eventCount:

                    eventIndex = r.random()*sum(HISTORIC_EVENT_CHANCES.values())

                    Event = None
                    for ev in HISTORIC_EVENTS:
                        eventIndex -= HISTORIC_EVENT_CHANCES[ev]
                        if eventIndex<=0:
                            Event = ev
                            break

                    event = Event(pos,year,context)

                    while event.getAlternateEvent():
                        event = event.getAlternateEvent()
                        
                    if not event.getSuccessful():
                        continue

                    historyMap.addEvent(event)
                    
                    i+=1

    for loc in historyMap.getLocations():
        if not loc.getCurrentState().existing:
            loc.destroy(context)
    
    return historyMap
        
        
def displayHistoryExplorer(historyMap, historyLen):
    historyMap.getCharacters().sort(key=lambda c: c.getBirthTime())
    charDecadeMenu = Menu([],"Characters",(0,255,0))
    for decade in range(0,historyLen,10):
        characterMenu = Menu([],"%i-%i" % (decade,decade+9),(255,128,0))
        for c in historyMap.getCharacters():
            if c.getBirthTime() in range(decade,decade+10):
                characterMenu.addElement( List(c.getEventDescriptions(),c.getName()) )
            
        charDecadeMenu.addElement(characterMenu)

    locDecadeMenu = Menu([],"Locations",(0,255,0))
    for decade in range(0,historyLen,10):
        characterMenu = Menu([],"%i-%i" % (decade,decade+9),(255,128,0))
        for loc in historyMap.getLocations():
            if loc.getCreationTime() in range(decade,decade+10):
                characterMenu.addElement( List(loc.getEventDescriptions(),loc.getName()) )
            
        locDecadeMenu.addElement(characterMenu) 
    
    superMenu = Menu([charDecadeMenu,locDecadeMenu],"",(255,255,255))
    createMenuWindow(superMenu)





            

    
