#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Team(object):
    def __init__(self, seed, name=None):
        # seed - integer [1,16]
        # region - str, used for debugging
        # name - str
        self.seed = seed
        # self.region = region
        self.name = name

    def getSeed(self):
        return self.seed
##    def getRegion(self):
##        return self.region
    def getName(self):
        return self.name
    def getJSON(self):
        return {"seed" : self.seed, "name" : self.name}
    def __str__(self):
        if self.name == None:
            return str(self.seed) # + " from region " + str(self.region)
        else:
            return "(" + str(self.seed) + ") " + self.name
