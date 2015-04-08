#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
from lib.database import generateJSON

args = cgi.FieldStorage()

print "Content-Type: application/json"
print ""
if "id" in args.keys():
	print generateJSON(args["id"].value)
else:
        print generateJSON()
	# print generateJSON("104832b2935a8650")
