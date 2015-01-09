#!/usr/bin/env python

from itertools import izip
import random, time, datetime, binascii, os

# MATCH OBJECT: REPRESENTS ONE GAME BETWEEN TWO TEAMS
class Match(object):
    def __init__(self, value, child1, child2):
        # value - winner, Team object
        # child1, child2 - competitors, 2 Match objects
        self.validate(value, child1, child2)

        self.child1 = child1
        self.child2 = child2
        self.value = value

    # ERROR CHECKING METHOD - ALWAYS CALL BEFORE SETTING INSTANCE VARIABLES
    def validate(self, value, child1, child2):
        if value is not None: # allow undecided matches
            if (child1 is None) != (child2 is None): # xor
                raise ValueError("When setting the value, only both or neither children can be None.")
            if (child1 is not None) or (child2 is not None): # allow first-round Nodes with a value but no children
                if (value != child1.getValue() and value != child2.getValue()):
                    raise ValueError("Only child1, child2, and None can be valid values.")
    
    def setValue(self, value):
        self.validate(value, self.child1, self.child2)
        self.value = value

    def setChild1(self, child1):
        self.validate(value, child1, self.child2)
        self.child1 = child1

    def setChild2(self, child2):
        self.validate(value, self.child1, child2)
        self.child2 = child2

    def getValue(self):
        return self.value
    def getWinner(self):
        return self.value
    def getChild1(self):
        return self.child1
    def getChild2(self):
        return self.child2

    def getTeams(self):
        return (self.child1.getValue(), self.child2.getValue())
    
    def getLoser(self): # return team object of loser
        if self.child1 is None or self.child2 is None:
            return None
        if self.child1.getValue() == self.value:
            return self.child2.getValue()
        if self.child2.getValue() == self.value:
            return self.child1.getValue()
        raise ValueError("Something is wrong with this match.")
    
    def __str__(self):
        if self.value is None: # no winner declared
            if self.child1 is None and self.child2 is None: # empty match
                return ""
            else: # undecided match
                return self.child1.getValue().__str__() + " vs " + self.child2.getValue().__str__()
        else:
            if self.child1 is None and self.child2 is None: # team == match, used for first round match child
                return ""
            else: # decided match
                if self.child1.getValue() == self.value:
                    return self.child1.getValue().__str__() + " defeated " + self.child2.getValue().__str__()
                else:
                    return self.child2.getValue().__str__() + " defeated " + self.child1.getValue().__str__()


# FUNCTION FOR PAIRWISE ITERATION THROUGH A LIST
def pairwise(iterable):
    # "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

matchorder = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15]

# BRACKET OBJECT: REPRESENTS 64-TEAM BRACKET DIVIDED INTO 4 REGIONS
class Bracket(object):
    def __init__(self, teams):
        # teams - array of dicts as specified in teams.py

        self.matches = []

        # round of 64
        thisround = []
        for region in teams:
            for seed1, seed2 in pairwise(matchorder):
                m1 = Match(region[str(seed1)],None,None)
                m2 = Match(region[str(seed2)],None,None)
                thisround.append(Match(None,m1,m2))
        self.matches.append(thisround)

        # round of 32
        thisround = []
        for match1, match2 in pairwise(self.matches[0]):
            thisround.append(Match(None,match1,match2))
        self.matches.append(thisround)

        # round of 16
        thisround = []
        for match1, match2 in pairwise(self.matches[1]):
            thisround.append(Match(None,match1,match2))
        self.matches.append(thisround)

        # round of 8 - quarterfinals
        thisround = []
        for match1, match2 in pairwise(self.matches[2]):
            thisround.append(Match(None,match1,match2))
        self.matches.append(thisround)

        # round of 4 - semifinals
        thisround = []
        for match1, match2 in pairwise(self.matches[3]):
            thisround.append(Match(None,match1,match2))
        self.matches.append(thisround)

        # round of 2 - championship game
        thisround = []
        for match1, match2 in pairwise(self.matches[4]):
            thisround.append(Match(None,match1,match2))
        self.matches.append(thisround)

    def getMatches(self):
        return self.matches

    def getBitRepresentation(self): # for storage in database
        result = "1" # force every bit to appear
        for rnd in self.matches:
            for match in rnd:
                result += str(int(match.getTeams().index(match.getValue())))
        return int(result,2) # resulting bitstring is 64-bits long, including leading bit
    
    def __str__(self):
        result = ""
        rndnum = 2
        for rnd in self.matches:
            result += ("Round " + str(rndnum) + "\n")
            for match in rnd:
                result += (match.__str__() + "\n")
            rndnum += 1
            result += "\n"
        return result


# PROBABILITY FUNCTIONS
def win(team1, team2, rndnum):
    if random.random() < winProb(team1, team2, rndnum):
        return team1
    else:
        return team2
    # return (team1 if r < winProb(team1, team2, rnd) else team2)

def winProb(team1, team2, rndnum):
    a = alpha(team1, team2, rndnum)
    seed1 = int(team1.getSeed())
    seed2 = int(team2.getSeed())
    return 1.0 * seed2**a / (seed1**a + seed2**a)

def alpha(team1, team2, rndnum):
    return 1 # TODO: replace with actual function

# RUN THROUGH BRACKET
def determineWinners(bracket, bitstring=None):
    # bitstring (long int) - a 64-bit bitstring starting with 1
    rndnum = 2
    if bitstring is None: # generate new bracket according to model
        for rnd in bracket.getMatches():
            for match in rnd:
                team1 = match.getChild1().getValue()
                team2 = match.getChild2().getValue()
                match.setValue(win(team1,team2,rndnum))
            rndnum += 1
    else: # generate new bracket according to bitstring
        bitpos = 1
        bits = str(bitstring)
        for rnd in bracket.getMatches():
            for match in rnd:
                currentBit = bits[bitpos]
                if bool(int(currentBit)):
                    match.setValue(match.getChild2().getValue())
                else:
                    match.setValue(match.getChild1().getValue())
                bitpos += 1
            rndnum += 1

def getTimestamp():
    return datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def getUniqueID():
    return binascii.b2a_hex(os.urandom(8))
