#!/usr/bin/env python

from bracket import *
from teams import getTeams
# from web import load_default_browser

# TODO: first four?
# TODO: alpha function, separate file?
# TODO: bracket stored in database
# TODO: email generated bracket (HTML to PDF?)

if __name__ == "__main__":
    import cProfile
    
    #print "March Madness 2014 Simulator"
    #print "\n"

    b = Bracket(getTeams())
    #cProfile.run("determineWinners(b)")
    # print timeit.timeit("determineWinners(b)", setup="from bracket import *")
    #determineWinners(b)

    for i in range(0,1):
        determineWinners(b)

    #print b
    #print bin(b.getBitRepresentation())

# use str.format(html, *(args)) with {}
