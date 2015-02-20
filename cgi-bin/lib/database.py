#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.bracket import *
from lib.teams import getTeams
import os
import lxml.html
import MySQLdb


def connect():
    return MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
                           user="ayang14_ncaa",
                           passwd="roflcopter1",
                           db="ayang14_marchmadness")


def insert(timestamp, uniqueID, binary):
    db = connect()
    cur = db.cursor()
    command = ("INSERT INTO ayang14_marchmadness.Bracket "
               "(timestamp, id, bitstring) "
               "VALUES (\"{0}\",\"{1}\",{2})".format(timestamp, uniqueID, binary))
    try:
        cur.execute(command)
        db.commit()
    except MySQLdb.Error as e:
        db.rollback()
        raise e
    finally:
        db.close()
        cur.close()


def select(uniqueID):
    # returns tuple: (timestamp, binary)
    db = connect()
    cur = db.cursor()
    command = ("SELECT timestamp, bitstring FROM ayang14_marchmadness.Bracket "
               "WHERE id=\"{0}\"".format(uniqueID))
    cur.execute(command)
    rows = cur.fetchall()
    db.close()
    cur.close()
    return rows[0]


def isValidID(ID):
    # Valid IDs are:
    # 1. Made of only hex chars.
    # 2. Exactly 16 chars long.
    # 3. Str type.
    if len(ID) == 16:
        try:
            int(ID, 16)
            return True
        except ValueError:
            return False
    else:
        return False


def generate(uniqueID=None):
    # returns an HTML string

    mustGenerateNewBracket = uniqueID is None
    b = Bracket(getTeams())
    if not mustGenerateNewBracket:
        timestamp, bitstring = select(uniqueID)
    else:
        bitstring = None
    determineWinners(b, bitstring)

    f = open("./templates/bracket.html")
    page = lxml.html.fromstring(f.read())
    f.close()

    # modify bracket DOM
    rndnum = 2
    for rnd in b.getMatches():
        matchnum = 1
        for match in rnd:
            # child1
            el = page.cssselect("#{0}r{1}".format(matchnum, rndnum))[0]
            team = match.getTeams()[0]
            el.cssselect(".seed")[0].text = str(team.getSeed())
            el.cssselect(".name")[0].text = team.getName()
            matchnum += 1
            if team is match.getValue():
                el.attrib["class"] += " winner"

            # child2
            el = page.cssselect("#{0}r{1}".format(matchnum, rndnum))[0]
            team = match.getTeams()[1]
            el.cssselect(".seed")[0].text = str(team.getSeed())
            el.cssselect(".name")[0].text = team.getName()
            matchnum += 1
            if team is match.getValue():
                el.attrib["class"] += " winner"
        rndnum += 1

    champion = page.cssselect("#champion")[0]
    champion.cssselect(".seed")[0].text = match.getValue().getSeed()
    champion.cssselect(".name")[0].text = match.getValue().getName()

    page.cssselect("#first-region")[0].text = "SOUTH" # top-left
    page.cssselect("#second-region")[0].text = "EAST" # bottom-left
    page.cssselect("#third-region")[0].text = "MIDWEST" # bottom-right
    page.cssselect("#fourth-region")[0].text = "WEST" # top-right

    # generate debug info
    if mustGenerateNewBracket:
        timestamp = getTimestamp()
        bitstring = bin(b.getBitRepresentation())[2:]  # eliminate leading 0b
        success = False
        while not success:
            try:
                uniqueID = getUniqueID()
                insert(timestamp, uniqueID, bitstring)
                success = True
            except MySQLdb.Error as e:
                if e[0] != 1062:  # error code 1062: duplicate ID
                    raise e

    # modify debug DOM
    debug = page.cssselect(".debug")[0]
    debug.cssselect("#time")[0].text = "This bracket was generated on {0} UTC".format(timestamp)
    if mustGenerateNewBracket:
        debug.cssselect("#link")[0].cssselect("a")[0].set("href", "/cgi-bin/bracket.py?id={0}".format(uniqueID))
        debug.cssselect("#link")[0].cssselect("a")[0].text = "Permalink to generated bracket"
        page.cssselect("#refreshmessage")[0].cssselect("a")[0].text = "Refresh this page for another bracket."
    else:
        debug.cssselect("#link")[0].cssselect("a")[0].set("href", "/bracket")
        debug.cssselect("#link")[0].cssselect("a")[0].text = "Generate another bracket"
        page.cssselect("#refreshmessage")[0].cssselect("a")[0].text = "Click here for another bracket."
    return lxml.html.tostring(page, pretty_print=True)
