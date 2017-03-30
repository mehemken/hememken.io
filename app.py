#!/usr/bin/env python

import sys
import os
import logging

from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--build',
        help='Build the static site.',
        action='store_true')
parser.add_argument('-p', '--path',
        help='Print the build path.',
        action='store_true')

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

build_path = '../build/'
# os_result = os.path.abspath(build_path)
FREEZER_DESTINATION = build_path


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    page = pages.get_or_404('index')
    return render_template('default.html', page=page)
    # return render_template('index.html')

@app.route('/about/')
def about():
    page = pages.get_or_404('about')
    return render_template('default.html', page=page)

if __name__ == '__main__':
    handler = RotatingFileHandler('logs/mehemken.io.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    args = parser.parse_args()

    if args.path:
        app.logger.info(FREEZER_DESTINATION)
        sys.exit()

    if args.build:
        app.logger.info('Do you want to build?')
        ans = input('yes/no: ')
        if ans == 'yes':
            try:
                freezer.freeze()
            except:
                app.logger.exception('There was an exception during the freeze.')
        else:
            app.logger.info('build aborted')
    else:
        app.run(debug=True)
