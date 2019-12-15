from game.game import Game

def startGameAt(world,location):
    game = Game(world,location)
    game.run()
