from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import random as r
import copy


class HEvCreateMasterPiece(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)
        
        char = None
        for c in characters:
            if (c.getCurrentState().alive
                and c.getCurrentState().occupation.craftsman
                and len(c.getCurrentState().items) < 1
                and c.getCurrentState().getAttributes().getMind()>=r.randint(1,14)):
                char = c
                break

        if not char:
            self.setSuccessful(False)
            return
        
        self.createdItem = char.getCurrentState().occupation.creationType(char.getCurrentState().occupationLevel)
        super().__init__(char.getCurrentState().livingPlace.getPos(),time,[char],context)
        self.updateCharacters()

    def getModifiedCharacterState(self,character,state):
        if character == self.getCharacters()[0]:
            newState = copy.copy(state)
            newState.items.append(self.createdItem)
            newState.itemsOnSale.append(self.createdItem)
            return newState
        return state

    def getDescription(self,character):
        return "%s created a master piece %s in %i" % (character.getName(),self.createdItem.name,self.getTime())



class HEvBuyMasterpiece(HistoricEvent):
    def __init__(self,pos,time,context):
        characters = context.getHistoryMap().getCharacters()
        r.shuffle(characters)
        
        for char in characters:
            
            if not (char.getAge(time)>=char.getCurrentState().getRace().adultAge
                and char.getCurrentState().alive
                and len(char.getCurrentState().items) < r.randint(1,3)
                and not (not char.getCurrentState().occupation.warrior and r.random()<0.5)):
                continue

                
            
            boughtItem = None
            seller = None
            for c in char.getCurrentState().livingPlace.getCurrentCharacters(time):
                if (c.getCurrentState().itemsOnSale
                    and c!=char
                    and c.getCurrentState().alive):

                    boughtItem = None
                    for item in c.getCurrentState().itemsOnSale:
                        
                        if item.quality > char.getCurrentState().occupationLevel + r.randint(-1,1):
                            continue
                        if item.art and char.getCurrentState().occupation.warrior:
                            continue

                        boughtItem = item
                        break

                    if boughtItem:
                        seller = c
                        break

            if not seller:
                continue
            self.seller = seller
            self.buyer = char
            self.item = boughtItem
            self.importantItem = r.random()<0.5

            super().__init__(self.seller.getCurrentState().livingPlace.getPos(),time,[self.seller,self.buyer],context)
            self.updateCharacters()
            return
        
        self.setSuccessful(False)
        return
        
    def getModifiedCharacterState(self,character,state):
        if character == self.buyer:
            newState = copy.copy(state)
            newState.items.append(self.item)
            return newState
        
        if character == self.seller:
            newState = copy.copy(state)
            newState.items.remove(self.item)
            newState.itemsOnSale.remove(self.item)
            return newState
        return state

    def getDescription(self,character):
        if character==self.buyer:
            return "%s bought masterpiece %s from %s in %i" % (character.getName(),self.item.name,self.seller.getName(),self.getTime())
        else:
            return "%s sold masterpiece %s to %s in %i" % (character.getName(),self.item.name,self.buyer.getName(),self.getTime())



class HEvAcquireLeftItem(HistoricEvent):
    def __init__(self,pos,time,context):
        self.location = None
        r.shuffle(context.getHistoryMap().getLocations())

        for loc in context.getHistoryMap().getLocations():
            if loc.getCurrentCharacters(time) and loc.getCurrentState().storedItems:
                self.location = loc
                break
        
        if not self.location :
            self.setSuccessful(False)
            return

        self.character = r.choice(self.location.getCurrentCharacters(time))
        
        self.item = r.choice(self.location.getCurrentState().storedItems)

        super().__init__(self.location.getPos(),time,
                         [self.character],context,[self.location])
        self.updateCharacters()
        self.updateLocations()

    def getModifiedCharacterState(self,character,state):
        if character == self.character:
            newState = copy.copy(state)
            newState.items.append(self.item)
            return newState
        return state

    def getModifiedLocationState(self,location,state):
        if location == self.location:
            newState = copy.copy(state)
            newState.storedItems.remove(self.item)
            return newState
        return state

    def getDescription(self,character):
        return "%s found %s in %s in %i" % (self.character.getName(),self.item.getName(), self.location.getName(),
                                            self.getTime())

    def getLocationDescription(self,location):
        return self.getDescription(self.character)
