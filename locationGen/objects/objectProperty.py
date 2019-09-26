
class ObjectPropertyType:
    OPT_DESCRIPTION = object() #requires "int getDescrPriority(self)", "str getName(self)" and "str getDescription(self)"
    OPT_CONTAINER = object() #requires "list getItems(self)", "int getSize(self)", "bool addItem(self,item)" and "removeItem(self,item)"
    OPT_INIT = object() #requires "onInit(self)" - gets called when object is initialized

class ObjectPropertyTemplate:
    def __init__(self,property,args):
        self.property = property
        self.args = args

    def instantiate(self,object):
        return self.property(object,*self.args)

class ObjectProperty:
    def __init__(self,object):
        self.object = object
    def getObject(self):
        return self.object
    def getTypes(self):
        return []


class ObjectDescriptionProperty(ObjectProperty):
    def __init__(self,object,name,descPrio=0):
        self.name = name
        self.descPrio = descPrio
        super().__init__(object)

    def getTypes(self):
        return [ObjectPropertyType.OPT_DESCRIPTION]

    def getDescrPriority(self):
        return self.descPrio

    def getName(self):
        return self.name

    def getDescription(self):
        return "an " if self.name[0].lower() in "aeiou" else "a " + self.name


class ObjectContainerProperty(ObjectProperty):
    def __init__(self,object,size,contents=[]):
        self.size = size
        self.contents = list(contents)
        super().__init__(object)

    def getTypes(self):
        return [ObjectPropertyType.OPT_CONTAINER]

    def getItems(self):
        return self.contents

    def getSize(self):
        return self.size

    def addItem(self,item):
        self.contents.append(item)
        return len(self.contents) >= self.getSize()

    def removeItem(self,item):
        self.contents.remove(item)


class LootGeneratorProperty(ObjectProperty):
    def __init__(self,object,lootTable,lootChance=0.5):
        self.lootTable = lootTable
        self.lootChance = lootChance
        super().__init__(object)

    def getTypes(self):
        return [ObjectPropertyType.OPT_INIT]

    def onInit(self):
        container = self.getObject().getProperty(ObjectPropertyType.OPT_CONTAINER)
        items = self.lootTable.getRandomObjects(container.getSize(), self.lootChance)
        for i in items:
            container.addItem(i.instantiate(None))
