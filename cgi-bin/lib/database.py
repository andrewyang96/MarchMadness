#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.bracket import *
from lib.teams import getTeams
import os
import MySQLdb

TABLE = "bracketo_marchmadness"

def connect():
    return MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
                           user="bracketo_client",
                           passwd="M@rchM@dn355",
                           db="bracketo_marchmadness")


def insert(timestamp, uniqueID, binary):
    db = connect()
    cur = db.cursor()
    command = ("INSERT INTO {0}.Bracket "
               "(timestamp, id, bitstring) "
               "VALUES (\"{1}\",\"{2}\",{3})".format(TABLE, timestamp, uniqueID, binary))
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
    command = ("SELECT timestamp, bitstring FROM {0}.Bracket "
               "WHERE id=\"{1}\"".format(TABLE, uniqueID))
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

import json

def generateJSON(uniqueID=None):
    # returns an HTML string

    mustGenerateNewBracket = uniqueID is None
    teams = getTeams()
    b = Bracket(teams)
    if mustGenerateNewBracket:
        bitstring = None
        determineWinners(b, bitstring)
        bitstring = bin(b.getBitRepresentation())[2:] # eliminate leading 0b
        timestamp = getTimestamp()
        success = False
        while not success:
            try:
                uniqueID = getUniqueID()
                insert(timestamp, uniqueID, bitstring)
                success = True
            except MySQLdb.Error as e:
                if e[0] != 1062:  # error code 1062: duplicate ID
                    raise e
    else:
        timestamp, bitstring = select(uniqueID)
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        determineWinners(b, bitstring)

    # calculate score
    score, gamesCorrect = calculateScore(b)
    matcheslist = [[[team.getJSON() for team in match.getTeams()] for match in rnd] for rnd in b.getMatches()]
    return json.dumps({"bitstring": bitstring, "timestamp": timestamp, "uniqueID": uniqueID, "matches": matcheslist, "isNew": mustGenerateNewBracket, "score": score, "gamesCorrect": gamesCorrect})
