#!/usr/bin/python

import CGIHTTPServer
import BaseHTTPServer
# import os

##path = os.path.dirname(os.path.realpath(__file__))
##print path+"/cgi"

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]

PORT = 3000

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()
