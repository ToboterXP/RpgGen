

class LocationType:
    def __init__(self,tags,rootContentCollection,name="", attachTags=[],propertyTemplates=[]):
        self.tags = tags
        self.rootContentCollection = rootContentCollection
        self.attachTags = attachTags
        self.name = name
        self.propertyTemplates = list(propertyTemplates)
