
import random as r
import randomUtil as ru


class LocationContentCollection:
    EMPTY = None
    def __init__(self,items,countRange,tags,organize):
        self.items = items
        self.countRange = countRange
        self.tags = tags
        self.organize = organize

    def getTags(self):
        return self.tags

    def getItems(self):
        return self.items

    def generateLocations(self,given,taken,superConnections,superLocation):
        content = []

        if not self.items:
            return []

        for g in given:
            isMatch = True
            for tag in g.getTags():
                if not tag in self.getTags():
                    isMatch = False
            if isMatch:
                content.append(g)

        givenLocs = []
        for g in content:
            given.remove(g)
            taken.append(g)
            givenLocs.append(g.getLocation(given,ru.getRandomSeed()))
        content = givenLocs


        itemCount = r.choice(self.countRange)
        sItems = list(self.items)
        r.shuffle(sItems)
        for item in sItems:
            if item.getItems():
                content += item.generateContent(given)
            else:
                content.insert(0,item.getLocation(given,ru.getRandomSeed()))

            itemCount -= 1
            if itemCount<=0:
                break

        for i in range(itemCount):
            item = r.choice(sItems)
            if item.getItems():
                content += item.generateContent(given)
            else:
                content.insert(0,item.getLocation(given,ru.getRandomSeed()))

        self.organize(content,superConnections,superLocation)
        return content

LocationContentCollection.EMPTY = LocationContentCollection([],range(0),[],lambda n: n)
