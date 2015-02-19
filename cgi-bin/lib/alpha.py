#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
path = os.path.dirname(os.path.realpath(__file__)) + "/"

def getAlphaFile(rndnum):
    alphas = {}
    with open(path + "data/alpha" + str(rndnum) + ".txt", "r") as data:
        for line in data:
            line = line.strip()
            l = line.split(",")
            l[:] = [float(s) for s in l]
            l[0], l[1] = int(l[0]), int(l[1])
            alphas[tuple(l[:-1])] = l[-1]
    return alphas
