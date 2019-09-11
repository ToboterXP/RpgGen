import pygame as pg
pg.init()

FONT = pg.font.Font(pg.font.match_font("Helvetica",bold=True),14)

class Text:
    def __init__(self,text,title):
        self.text = text
        self.title = title
        self.menu = False

    def getTitle(self):
        return self.title

    def draw(self, display, pos, scrollPos):
        pos = list(pos)
        for line in self.text.split("\n"):
            display.blit( FONT.render(line, True, (255,255,255)), pos)
            pos[1] += 14

class List:
    def __init__(self,texts,title):
        self.texts = texts
        self.title = title
        self.menu = False

    def getTitle(self):
        return self.title

    def draw(self, display, pos, scrollPos):
        pos = list(pos)
        for text in self.texts[scrollPos%len(self.texts):]:
            for line in text.split("\n"):
                display.blit( FONT.render(line, True, (255,255,255)), pos)
                pos[1] += 14
            pos[1] += 12
            

class Menu:
    def __init__(self, elements, name, color):
        self.elements = elements
        self.name = name
        self.color = color
        self.focused = False
        self.selectedIndex = 0
        self.menu = True
        self.super = None
        self.currentScrollPos = 0

        for e in elements:
            if e.menu:
                e.setSuper(self)

    def getElements(self):
        return self.elements

    def addElement(self,element):
        self.elements.append(element)
        if element.menu:
            element.setSuper(self)

    def setSuper(self,sup):
        self.super = sup

    def passFocus(self,index):
        self.focused = True
        self.currentScrollPos = 0
        self.setFocusLine(self.elements[min(len(self.elements)-1, index)])

    def setFocusLine(self,element):
        self.selectedIndex = self.elements.index(element)
        if self.super:
            self.super.setFocusLine(self)

    def getTitle(self):
        return self.name

    def searchFor(self,term):
        for e in self.elements:
            if e.menu:
                if e.searchFor(term):
                    return True
            else:
                if e.getTitle() == term:
                    self.passFocus(self.elements.index(e))
                    return True
        return False

    def draw(self, display, pos, scrollPos):
        if not self.elements:
            return
        elementPos = list(pos)
        i = max(0,self.selectedIndex-30)
        for element in self.elements[ i :]:
            cursor = ""
            if i == self.selectedIndex and self.focused:
                cursor = "> "
            display.blit( FONT.render(cursor + element.getTitle(), True, self.color), elementPos)
            elementPos[1] += 18

            i+= 1

        pos = list(pos)
        pos[0] += 150
        self.elements[self.selectedIndex].draw(display, pos, self.currentScrollPos)

    def handleInput(self,key):
        if key == pg.K_s:
            done = False
            while not done:
                search = input("Search: ")
                if self.searchFor(search):
                    self.focused = False
                    print("Found")
                    done = True
                else:
                    print("No result found")
                    if search=="":
                        done = True
            return
            
        if self.focused:
            if key == pg.K_UP:
                self.currentScrollPos = 0
                self.selectedIndex = (self.selectedIndex-1) % len(self.elements)
                
            if key == pg.K_DOWN:
                self.currentScrollPos = 0
                self.selectedIndex = (self.selectedIndex+1) % len(self.elements)
                
            if key == pg.K_RIGHT:
                 if self.elements[self.selectedIndex].menu and self.elements[self.selectedIndex].getElements():
                    self.elements[self.selectedIndex].passFocus(0)
                    self.focused = False
                    
            if key == pg.K_LEFT:
                if self.super:
                    self.super.passFocus(self.super.getElements().index(self))
                    self.focused = False
                    self.selectedIndex = 0

            if key == pg.K_KP_PLUS:
                self.currentScrollPos += 1
            if key == pg.K_KP_MINUS:
                self.currentScrollPos -= 1
        else:
            self.elements[self.selectedIndex].handleInput(key)


def createMenuWindow(menu):
    menu.passFocus(0)
    display = pg.display.set_mode((1000,800),0,0)

    pressed = []
    while True:
        display.fill((0,0,0))
        menu.draw(display, (10,10), 0)
        pg.display.flip()

        for event in pg.event.get(): 
            if event.type==pg.QUIT:
                pg.quit()
                return False

        for key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_s, pg.K_KP_PLUS, pg.K_KP_MINUS):
            if pg.key.get_pressed()[key]:
                if not key in pressed:
                    menu.handleInput(key)
                    pressed.append(key)
            else:
                if key in pressed:
                    pressed.remove(key)
        

if __name__=="__main__":
    
    testText1 = Text("This is\nsome test text","Test")
    testText2 = Text("This is just some other test text","Test2")

    testList1 = List(["Hydrogen","Helium","Lithium","Beryllium"],"Elements")

    testMenu = Menu((testText1, testText2), "TestMenu", (255,128,0))
    testMenu2 = Menu((testText2, testList1), "TestMenu2", (255,0,0))

    testMenu3 = Menu((testMenu, testMenu2),"",(0,255,0))

    createMenuWindow(testMenu3)











                  
        
    
