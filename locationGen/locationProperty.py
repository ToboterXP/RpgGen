import randomTextTemplate as rtt
import randomUtil as ru


class LocationPropertyType:
    LPT_DESCRIPTION = object() #requires "getDescPrority(self)" and "getDescription(self)"
    LPT_INIT = object() #requires "onInit(self)"
    LPT_CONTEXT = object() #requires "getContextName(self)" and "getContext(self)"


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
        ret = self.property(location,*self.args)

        if LocationPropertyType.LPT_INIT in ret.getTypes():
            ru.pushNewSeed()
            ret.onInit()
            ru.popSeed()

        return ret


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

class ContextProperty(LocationProperty):
    def getTypes(self):
        return [LocationPropertyType.LPT_CONTEXT]

    def __init__(self,location,name,context):
        self.name = name
        self.context = context
        super().__init__(location)

    def getContextName(self):
        return self.name

    def getContext(self):
        return self.context
