import randomTextTemplate as rtt


class LocationPropertyType:
    LPT_DESCRIPTION = object() #requires "getDescPrority(self)" and "getDescription(self)"
    LPT_INIT = object() #requires "onInit(self)"


class LocationProperty:
    def __init__(self,location):
        self.location = location

    def getLocation(self):
        return self.location

    def getTypes(self):
        return []

class LocationPropertyTemplate:
    def __init__(self,property,args):
        self.args = args
        self.property = property

    def instantiate(self,location):
        return self.property(location,*self.args)


class BasicDescriptionPropertyTemplate(LocationPropertyTemplate):
    def __init__(self,prio,descriptionTemplate):
        self.descriptionTemplate = descriptionTemplate
        self.prio = prio

    def instantiate(self,location):
        return BasicDescriptionProperty(rtt.generateText(self.descriptionTemplate),self.prio,location)

class BasicDescriptionProperty(LocationProperty):
    def getTypes(self):
        return [LocationPropertyType.LPT_DESCRIPTION]

    def __init__(self,description,prio,location):
        self.description = description
        self.prio = prio
        super().__init__(location)

    def getDescPrority(self):
        return self.prio

    def getDescription(self):
        return self.description

class RandomObjectsProperty(LocationProperty):
    def getTypes(self):
        return [LocationPropertyType.LPT_INIT]

    def __init__(self,location,lootTable,amount,failChance=0.5):
        self.lootTable = lootTable
        self.amount = amount
        self.failChance = failChance
        super().__init__(location)

    def onInit(self):
        for obj in self.lootTable.getRandomObjects(self.amount,self.failChance):
            obj.instantiate(self.location)
