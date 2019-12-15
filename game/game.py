import pygame as pg
import graphicMenus as gm
from util import *
pg.init()

FONT = pg.font.Font(pg.font.match_font("Helvetica",bold=True),14)

class Game:
    GAME = None
    def __init__(self,world,location):
        self.world = world
        self.location = None
        self.startLocation = location
        Game.GAME = self
        self.display = pg.display.set_mode((1000,800),0,0)
        self.interactionMenu = None
        self.pressed = []

        self.move(location)
        self.reloadInteractions()



    def move(self,loc):
        if self.location and loc.isTopLocation():
            self.location.getTopLocation().unloadContent()
        self.location = loc
        self.location.loadContent()
        self.location = self.location.getFirstRoom()

    def doInteraction(self,handle,args):
        handle(*args)
        self.reloadInteractions()

    def reloadInteractions(self):
        interactions = []
        interactionHandles = self.location.getInteractionHandles()
        for inter in interactionHandles.keys():
            interactions.append( gm.InteractableText(inter,lambda inter: self.doInteraction(inter,tuple()), (interactionHandles[inter],)) )

        targets = []
        for c in self.location.getConnections():
            target = c.getSimplifiedConnection().getOther(self.location)
            interactions.append( gm.InteractableText("Move to "+ target.getName(), lambda inter,args: self.doInteraction(inter,args), (lambda t: self.move(t), (target,)) ))

        self.interactionMenu = gm.Menu(interactions, "Interactions", (0,255,0))
        self.interactionMenu.passFocus(0)

    def drawLocationScreen(self):
        self.display.fill((0,0,0))
        text = self.location.getDescription()
        y = 10
        for line in text.split("\n"):
            self.display.blit( FONT.render(line, True, (255,255,255)), (10,y))
            y += 14

        self.interactionMenu.draw(self.display, Vector2(10,y+14),0)
        pg.display.flip()

        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                return False

        for key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_s, pg.K_KP_PLUS, pg.K_KP_MINUS, pg.K_RETURN):
            if pg.key.get_pressed()[key]:
                if not key in self.pressed:
                    self.interactionMenu.handleInput(key)
                    self.pressed.append(key)
            else:
                if key in self.pressed:
                    self.pressed.remove(key)

        return True

    def run(self):
        run = True
        while run:
            run = self.drawLocationScreen()
