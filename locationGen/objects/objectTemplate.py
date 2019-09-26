from locationGen.objects.locationObject import *

class ObjectTemplate:
    def __init__(self,propertyTemplates):
        self.propertyTemplates = propertyTemplates

    def instantiate(self,location):
        return LocationObject(location,self.propertyTemplates)

    def __add__(self,other):
        return ObjectTemplate(self.propertyTemplates + other.propertyTemplates)
