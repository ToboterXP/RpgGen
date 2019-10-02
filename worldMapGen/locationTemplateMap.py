from locationGen.locationTypes.village import *

class LocationTemplate:
    def __init__(self,locationType,civilized=False):
        self.locationType = locationType
        self.civilized = civilized

LOCATION_TEMPLATE_MAP = {
    "Village": LocationTemplate(BasicVillageType,True)
}
