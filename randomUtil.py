import random as r

currentRandoms = [r.Random()]
currentRandom = currentRandoms[0]

def getRandomSeed():
    return currentRandom.randint(-10000000000,10000000000)

def seed(s):
    pushSeed(s)

def pushNewSeed():
    pushSeed(getRandomSeed())

def pushSeed(seed):
    global currentRandom
    currentRandoms.append(r.Random(seed))
    currentRandom = currentRandoms[-1]

def popSeed():
    global currentRandom
    currentRandoms.pop()
    currentRandom = currentRandoms[-1]

def random():
    return currentRandom.random()

def randint(a,b):
    return currentRandom.randint(a,b)

def choice(l):
    return currentRandom.choice(l)

def shuffle(l):
    currentRandom.shuffle(l)
