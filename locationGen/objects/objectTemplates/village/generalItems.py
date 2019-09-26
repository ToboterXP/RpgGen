from locationGen.objects.objectProperty import *
from locationGen.objects.objectTemplate import *
from locationGen.objects.objectTemplates.basicObjects import *

#basic village loot
COMB = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("comb",5))
]) + BASIC_ITEM_TEMPLATE

EMPTY_BAG = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("empty bag",4)),
    ObjectPropertyTemplate(ObjectContainerProperty, (2,))
]) + BASIC_ITEM_TEMPLATE

HANDKERCHIEF = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("handkerchief",5))
]) + BASIC_ITEM_TEMPLATE

APPLE = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("apple",5))
]) + BASIC_ITEM_TEMPLATE

METAL_JUG = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("metal jug",5))
]) + BASIC_ITEM_TEMPLATE

PACK_OF_DICE = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("pack of dice",4))
]) + BASIC_ITEM_TEMPLATE

CHEAP_RING = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("cheap ring",4))
]) + BASIC_ITEM_TEMPLATE

PACK_OF_CARDS = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("pack of cards",4))
]) + BASIC_ITEM_TEMPLATE

WOODEN_FIGURINE = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("wooden figurine",5))
]) + BASIC_ITEM_TEMPLATE

LANTERN = ObjectTemplate([
    ObjectPropertyTemplate(ObjectDescriptionProperty, ("lantern",4))
]) + BASIC_ITEM_TEMPLATE
