from historyGen.historyEvents import *
from historyGen.historyCharacters import *
from historyGen.historyItems import *
from historyGen.historyLocations import *
import randomUtil as r
import copy

class HEvBattle(HistoricEvent):
    def __init__(self,pos,time,context,inevitable=False):
        participantNodes = context.getCloseLocations(pos,5,
                                                    sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().independant)

        startPart = None
        determination = 0
        for pn in participantNodes:
            p = pn.getAttachedContext(HistoryLocation)
            deter = p.getPersonality().determination+r.randint(-2,2)
            if (deter > determination):
                startPart = p
                determination = deter
                break

        if not startPart:
            self.setSuccessful(False)
            return

        if not inevitable and startPart.getPersonality().warmonger < r.randint(1,15):
            self.setAlternateEvent(HEvDiplomaticBattle(pos,time,context,inevitable=True))
            return

        self.participants = [startPart]


        self.reconquest = False

        lostLocations = []      #prevent conquest of own admin
        for l in startPart.getCurrentState().lostLocations:
            if l.getMainAdmin() != startPart.getMainAdmin():
                lostLocations.append(l)

        if lostLocations:
            self.reconquest = True
            self.participants.append(r.choice(lostLocations))
        else:
            for p in participantNodes:
                part = p.getAttachedContext(HistoryLocation)
                if part==startPart:
                    continue
                if ((part.getMainAdmin() != self.participants[0].getMainAdmin())
                and (not part in startPart.getCurrentState().friendlyLocations)):

                    self.participants.append(p.getAttachedContext(HistoryLocation))
                    break

        if len(self.participants)!=2:
            self.setSuccessful(False)
            return

        if abs(self.participants[0].getPos()-self.participants[1].getPos()) > 15:
            self.setSuccessful(False)
            return

        characters = []
        self.dyingCharacters = []
        for part in self.participants:
            for char in part.getCurrentCharacters(time):
                if (char.getAge(time) >= char.getCurrentState().getRace().adultAge
                    and char.getCurrentState().occupation.warrior):
                    characters.append(char)
                    if char.getCurrentState().getAttributes().getBody()<r.randint(1,12):
                        self.dyingCharacters.append(char)

        for c in characters:
            while characters.count(c)>1:
                characters.remove(c)

        winScore = [0,0]
        i=0
        for p in self.participants:
            winScore[i] += r.randint(0,2)
            for c in p.getCurrentCharacters(time):
                if not c in self.dyingCharacters and c.getCurrentState().occupation.warrior:
                    winScore[i] += 1
            i += 1

        if winScore[0]>winScore[1]:
            self.winner = self.participants[0]
            self.loser = self.participants[1]
        else:
            self.winner = self.participants[1]
            self.loser = self.participants[0]

        self.conquest = False
        if abs(winScore[0]-winScore[1])>r.randint(1,3):
            self.conquest = True

        if self.conquest:
            self.formerAdmin = self.loser.getCurrentState().adminLocation
            if self.formerAdmin:
                self.participants.append(self.formerAdmin)

        self.traumata = {}
        for c in characters:
            if (not c in self.dyingCharacters
                and c.getPersonality().determination<r.randint(5,15)
                and len(c.getCurrentState().personalityTraits)<4
                and c.getCurrentState().getAttributes().getMind()<r.randint(1,12)):

                trauma = r.choice(PersonalityTraits.TRAUMATIC_TRAITS)
                while trauma in c.getCurrentState().personalityTraits:
                    trauma = r.choice(PersonalityTraits.TRAUMATIC_TRAITS)
                self.traumata[c] = trauma

        self.spoils = []
        for c in self.dyingCharacters:
            self.spoils += c.getCurrentState().items

        self.aggressor = startPart.getCurrentState().leader
        if self.aggressor and not self.aggressor in characters:
            characters.append(self.aggressor)

        super().__init__(pos,time,characters,context,self.participants)
        self.updateCharacters()
        self.updateLocations()

    def getModifiedCharacterState(self,character,state):
        if character in self.dyingCharacters:
            newState = copy.copy(state)
            newState.alive = False
            newState.items = []
            newState.leadershipPos = None
            return newState
        elif character in self.getCharacters():
            newState = copy.copy(state)
            if character in self.traumata.keys():
                newState.personalityTraits.append(self.traumata[character])
            return newState
        return state

    def getModifiedLocationState(self,location,state):

        if location in self.participants:
            newState = copy.copy(state)

            if newState.leader in self.dyingCharacters:
                newState.leader = None

            if location==self.winner or location==self.loser:
                newState.associatedCharacters += self.getCharacters()

            if location == self.winner:
                newState.storedItems += self.spoils
                if self.conquest:
                    newState.subordinateLocs.append(self.loser)
                    if self.loser in newState.lostLocations:
                        newState.lostLocations.remove(self.loser)

            elif location == self.loser:
                if self.conquest:
                    newState.adminLocation = self.winner

            elif location == self.formerAdmin and self.conquest:
                newState.subordinateLocs.remove(self.loser)
                newState.lostLocations.append(self.loser)

            return newState
        return state

    def getDescription(self, character):
        if character in self.dyingCharacters:
            return "%s died in %i at war between %s and %s" % (character.getName(),
                                                                  self.getTime(),
                                                                  str(self.participants[0].getName()),
                                                                  str(self.participants[1].getName()))

        trauma = ""
        if character in self.traumata.keys():
            trauma = "\nreceiving trauma %s" % (self.traumata[character].name)
        warVerb = "takes part in"
        if character==self.aggressor:
            warVerb = "starts"
        return "%s in %i %s a war between %s and %s %s" % (character.getName(),
                                                            self.getTime(),
                                                           warVerb,
                                                            str(self.participants[0].getName()),
                                                            str(self.participants[1].getName()),
                                                            trauma)

    def getLocationDescription(self,location):
        characters = ""
        for c in self.getCharacters():
            characters += "\n" + c.getName()
        killedCharacters = ""
        for c in self.dyingCharacters:
            killedCharacters += "\n" + c.getName()
        spoils = ""
        for item in self.spoils:
            spoils += "\n"+item.getName()
        other = self.participants[0]
        if other==location:
            other = self.participants[1]

        verb = "lost"
        if location == self.winner:
            verb="won"
            if self.conquest:
                verb+=" and conquered"
            if self.reconquest:
                verb+=" as reconquest"
            verb += " in"
        elif self.conquest:
            verb += " and was conquered"
            if self.reconquest:
                verb+=" as reconquest"
            verb += " in"

        return "%s %s a war with %s in %i involving: %s \nkilling: %s\nSpoils: %s" % (location.getName(),
                                                                          verb,
                                                                          other.getName(),
                                                                         self.getTime(),
                                                                          characters,
                                                                          killedCharacters,
                                                                          spoils)




class HEvDiplomaticBattle(HistoricEvent):
    def __init__(self,pos,time,context,inevitable=False):
        participantNodes = context.getCloseLocations(pos,5,
                                                    sort=lambda n: n.getAttachedContext(HistoryLocation).getLocationType().independant)

        startPart = None
        determination = 0
        for pn in participantNodes:
            p = pn.getAttachedContext(HistoryLocation)
            deter = p.getPersonality().determination+r.randint(-2,2)
            if (deter > determination):
                startPart = p
                determination = deter
                break

        if not startPart:
            self.setSuccessful(False)
            return

        if not inevitable and startPart.getPersonality().warmonger >= r.randint(1,15):
            self.setAlternateEvent(HEvBattle(pos,time,context,inevitable=True))
            return

        self.participants = [startPart]


        for p in participantNodes:
            part = p.getAttachedContext(HistoryLocation)
            if part==startPart:
                continue
            if (part.getMainAdmin() != self.participants[0].getMainAdmin()
                and not part in startPart.getCurrentState().friendlyLocations):
                self.participants.append(p.getAttachedContext(HistoryLocation))
                break

        if len(self.participants)!=2:
            self.setSuccessful(False)
            return

        if abs(self.participants[0].getPos()-self.participants[1].getPos()) > 15:
            self.setSuccessful(False)
            return

        characters = []
        if startPart.getCurrentState().leader:
            characters = [startPart.getCurrentState().leader]

        super().__init__(pos,time,characters,context,self.participants)
        self.updateCharacters()
        self.updateLocations()

    def getModifiedCharacterState(self,character,state):
        return state

    def getModifiedLocationState(self,location,state):
        if location in self.participants:
            newState = copy.copy(state)
            for p in self.participants:
                if p!=location:
                    newState.friendlyLocations.append(p)
                    break
            return newState
        return state

    def getDescription(self, character):
        if character == self.getCharacters()[0]:
            return "%s solved the conflict between %s and %s\ndiplomatically in %i" % (character.getName(),self.participants[0].getName(),self.participants[1].getName(),self.getTime())
        return ""

    def getLocationDescription(self,location):
        if self.getCharacters():
            return self.getDescription(self.getCharacters()[0])
        else:
            return "%s and %s solved their conflict\ndiplomatically in %i" % (self.participants[0].getName(),self.participants[1].getName(),self.getTime())
