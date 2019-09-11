
from util import *

LOADED_TAGS = []
LOADED_OBJECTS = {}

def GetLoadedObjectClass(objectClass):
    try:
        return LOADED_OBJECTS[objectClass]
    except:
        raise Exception("Object class '%s' not loaded" % (objectClass) )

def LoadObjectFile(fileStream, objectClass):

    objects = []
    
    isObject = False
    currTagName = ""
    currParents = []
    color = (0,0,0)
    chance = 1
    lineNum = 0
    for line in fileStream.readlines() + ["tag a"]:
        lineNum += 1
        if line.startswith("atomic"):
            LOADED_TAGS.append( Tag(line.split(" ")[-1].replace("\n","")) )
            continue
        
        if line.startswith("tag") or line.startswith("object"):
            if currTagName!="":
                if not isObject:
                    LOADED_TAGS.append( Tag(currTagName, currParents) )
                else:
                    objects.append( TaggedObjectTemplate(currTagName, currParents, color, chance) )
            currTagName = line.split(" ")[-1].replace("\n","")
            currParents = []
            isObject = line.startswith("object")
            chance = 1
            continue

        if line.replace(" ","").replace("\n","") == "":
            continue

        if line.startswith("//"):
            continue

        if line.startswith("color"):
            parts = line.split(" ")
            color = (int(parts[1]),int(parts[2]),int(parts[3]))
            continue

        if line.startswith("chance"):
            chance = float(line.split(" ")[1])
            continue

        if line.startswith("require"):
            reqObjectClass = line.split(" ")[1].replace("\n","")
            try:
                GetLoadedObjectClass(reqObjectClass)
            except:
                raise Exception("Required object class '%s' not present for file %s" % (reqObjectClass,fileStream.name))
            continue

        poss = []
        for tagPoss in line.replace("\n","").split("|"):
            tagParts = tagPoss.replace("\n","").split(":")
            weight = 1
            if len(tagParts)>1:
                weight = float(tagParts[1])

            tag = None
            for t in LOADED_TAGS:
                if t.getName() == tagParts[0]:
                    tag = t
                    break

            if not tag:
                raise Exception("Unknown Tag reference '%s' in file %s, line %i" % (tagParts[0],fileStream.name,lineNum))

            poss.append( WeightedTag( tag, weight ))

        if isObject:
            currParents.append(poss)
        else:
            currParents.append(poss[0])

    LOADED_OBJECTS[objectClass] = objects
    

if __name__ == "__main__":
    with open("./tags/nature/combined.txt","r") as f:
        LoadObjectFile(f,"Biomes")

    for o in LOADED_OBJECTS["Biomes"]:
        print(o.name)
    print()

    for tag in LOADED_TAGS:
        print(tag.getName())
    
