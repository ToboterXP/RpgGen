from locationGen.objects.objectProperty import *
from locationGen.objects.objectTemplate import *
from locationGen.objects.objectTemplates.basicObjects import *
from locationGen.objects.lootTables.village.basicLoot import *



CUPBOARD = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("cupboard",5)),
    ObjectPropertyTemplate(ObjectContainerProperty, (4,)),
    ObjectPropertyTemplate(LootGeneratorProperty, (VILLAGE_BASIC_LOOT,0.3))
]) + BASIC_FURNITURE_TEMPLATE

CHEST = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("chest",5)),
    ObjectPropertyTemplate(ObjectContainerProperty, (4,)),
    ObjectPropertyTemplate(LootGeneratorProperty, (VILLAGE_BASIC_LOOT,0.3))
]) + BASIC_FURNITURE_TEMPLATE

SHELF = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("shelf",5)),
    ObjectPropertyTemplate(ObjectContainerProperty, (4,)),
    ObjectPropertyTemplate(LootGeneratorProperty, (VILLAGE_BASIC_LOOT,0.3))
]) + BASIC_FURNITURE_TEMPLATE

CHEST_OF_DRAWERS = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("chest of drawers",5)),
    ObjectPropertyTemplate(ObjectContainerProperty, (4,)),
    ObjectPropertyTemplate(LootGeneratorProperty, (VILLAGE_BASIC_LOOT,0.3))
]) + BASIC_FURNITURE_TEMPLATE

CHAIR = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("chair",5))
]) + BASIC_FURNITURE_TEMPLATE

TABLE = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("table",5))
]) + BASIC_FURNITURE_TEMPLATE
