
import randomUtil as r

class LootTable:
    def __init__(self,items,weights={}):
        self.weights = dict(weights)
        self.items = items
        for t in self.items:
            self.weights.setdefault(t,1)

    def getRandomObject(self):
        index = r.random()*sum(self.weights.values())
        for t in self.items:
            index -= self.weights[t]
            if index<=0:
                if t.__class__ == LootTable:
                    return t.getRandomObject()
                return t

    def getRandomObjects(self,number,failChance=0.5):
        ret = []
        for i in range(number):
            if r.random()<failChance:
                continue
            else:
                ret.append(self.getRandomObject())
        return ret
