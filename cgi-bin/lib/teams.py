#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from team import Team

# teams is an array of four dictionaries
# in each dict: the key is seed, and the value is the Team object
import os
path = os.path.dirname(os.path.realpath(__file__)) + "/"
# order may change
files = [path+"data/data_midwest.txt",
         path+"data/data_west.txt",
         path+"data/data_south.txt",
         path+"data/data_east.txt"]

# data files are csv of teams
# Specifications:
# First sixteen teams - South
# Second sixteen teams - East
# Third sixteen teams - Midwest
# Fourth sixteen teams - West
# Within each region: 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15

def getTeams():
    teams = []
    for f in files:
        regionname = ""
        if ("data_midwest" in f):
            regioninitial = "M"
        elif ("data_south" in f):
            regioninitial = "S"
        elif ("data_west" in f):
            regioninitial = "W"
        elif ("data_east" in f):
            regioninitial = "E"
        with open(f,"r") as data:
            region = {}
            for line in data:
                line = line.strip()
                # print line.split(",")
                line += "," + regioninitial
                teamobj = Team(*(line.split(",")))
                region[teamobj.getSeed()] = teamobj
            teams.append(region)
    return teams
