#!/usr/bin/env python

import sys
import os
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

os.chdir('..')
BUILD_PATH = os.getcwd()
os.chdir('app/')

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_DESTINATION = BUILD_PATH


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    page = pages.get_or_404('about')
    return render_template('about.html', page=page)

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        ans = input('continue? ')
        if ans == 'yes':
            freezer.freeze()
        else:
            logger.info('build aborted')
    else:
        app.run(debug=True)
