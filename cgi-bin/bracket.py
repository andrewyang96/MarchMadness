#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import datetime
import random
from lib.database import generate

args = cgi.FieldStorage()

print "Content-Type: text/html"
print ""
if "id" in args.keys():
	print generate(args["id"].value)
else:
	print generate()
