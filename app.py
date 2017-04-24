#!/usr/bin/env python

import sys
import os
import logging

from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from flask import Flask, render_template, url_for, send_from_directory
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

build_path = '../build/files'
FREEZER_DESTINATION = build_path


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    page = pages.get_or_404('index')
    resume = url_for('static', filename='resume/resume.pdf')
    return render_template('index.html', page=page, resume=resume)

@app.route('/resume/')
def resume():
    page = pages.get_or_404('index')
    resume = url_for('static', filename='resume/resume.pdf')
    return render_template('index.html', page=page, resume=resume)


if __name__ == '__main__':
    handler = RotatingFileHandler('logs/mehemken.io.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(debug=True)
