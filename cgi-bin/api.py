#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
from lib.database import generateJSON

# g = generateJSON("a154135adfacabc2")
# print g

args = cgi.FieldStorage()

print "Content-Type: application/json"
print ""
if "id" in args.keys():
	print generateJSON(args["id"].value)
else:
	print generateJSON()
