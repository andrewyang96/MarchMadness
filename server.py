#!/usr/bin/python

from flask import Flask, render_template, render_template_string, flash
import datetime
import random
from lib.database import generate

app = Flask(__name__)
app.secret_key = 'Z,\r\xb0<\x17\x11\x0bw\x06\x9f~\xa7\xa4y\xb1\x06\xaa\xdf2*s\xc7;'


@app.route("/", methods=["GET"])
def index_page():
	if app.debug:
		flash("Welcome to NCAA Bracket Generator")
	num = random.randint(0, 10)
	return render_template("index.html", num = num, dt = datetime.datetime.now())


@app.route("/bracket", methods=["GET"])
def generate_new_bracket():
	if app.debug:
		print "Generating new bracket"
	return render_template_string(generate())


@app.route("/bracket/<id>", methods=["GET"])
def generate_bracket(id):
	if app.debug:
		print "Bracket already generated:", id
	return render_template_string(generate(id))

if __name__ == "__main__":
    app.debug = False
    app.run()
