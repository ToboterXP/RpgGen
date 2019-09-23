
import random as r

class TextItem:
    def __init__(self,leftLimit,rightLimit):
        self.leftLimit = leftLimit
        self.rightLimit = rightLimit

    def generateText(self,itemContent):
        return itemContent

class MultiChoiceItem(TextItem):
    def __init__(self):
        super().__init__("[","]")

    def generateText(self,itemContent):
        return r.choice(itemContent.split("|"))

TEXT_ITEMS = [
    MultiChoiceItem()
]

def generateText(template, **keywords):
    for k in keywords.keys():
        if keywords[k].__class__ == list:
            keywords[k] = str(keywords[k]).replace(", ","|").replace("'","")
        else:
            keywords[k] = str(keywords[k])

    template = template.format(**keywords)

    currentItem = [TextItem("","")]
    currentContent = [""]
    itemStarts = {}

    for i in TEXT_ITEMS:
        itemStarts[i.leftLimit] = i

    for c in template:
        if c in itemStarts:
            currentItem.append(itemStarts[c])
            currentContent.append("")
        elif c == currentItem[-1].rightLimit:
            currentContent[-2] += currentItem[-1].generateText(currentContent[-1])
            currentItem.pop()
            currentContent.pop()
        else:
            currentContent[-1] += c

    return currentContent[0].replace("<","{").replace(">","}").format(**keywords)

if __name__=="__main__":
    while True:
        print(generateText(input("> "), test1="LOL", test2="XD", test3=["test","test2"]))
