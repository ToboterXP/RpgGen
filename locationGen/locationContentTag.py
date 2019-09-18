
class UIDTag:
    EXISTING_TAGS = {}
    def __init__(self,index):
        self.index = index
        UIDTag.EXISTING_TAGS[index] = self

    def getTagByIndex(index):
        ret = UIDTag.EXISTING_TAGS.get(index,None)
        if not ret:
            ret = UIDTag(index)
            UIDTag.EXISTING_TAGS[index] = ret
        return ret

VL_BUILDING = UIDTag(0)
VL_ROAD = UIDTag(1)

LEVEL_VILLAGE = UIDTag(2)
LEVEL_BUILDING = UIDTag(3)
LEVEL_ROOM = UIDTag(4)

RO_GEN_LIVING_QUARTER = UIDTag(5)
RO_GEN_SLEEPING_QUARTER = UIDTag(6)
