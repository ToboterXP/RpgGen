import randomTextTemplate as rtt


class LocationPropertyType:
    LPT_DESCRIPTION = object() #requires "getDescPrority(self)" and "getDescription(self)"


class LocationProperty:
    def getTypes(self):
        return []

class LocationPropertyTemplate:
    def instantiate(self,location):
        return LocationProperty()


class BasicDescriptionPropertyTemplate(LocationPropertyTemplate):
    def __init__(self,prio,descriptionTemplate):
        self.descriptionTemplate = descriptionTemplate
        self.prio = prio

    def instantiate(self,location):
        return BasicDescriptionProperty(rtt.generateText(self.descriptionTemplate),self.prio)

class BasicDescriptionProperty(LocationProperty):
    def getTypes(self):
        return [LocationPropertyType.LPT_DESCRIPTION]

    def __init__(self,description,prio):
        self.description = description
        self.prio = prio

    def getDescPrority(self):
        return self.prio

    def getDescription(self):
        return self.description
