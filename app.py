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

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# os.chdir('..')
# BUILD_PATH = os.getcwd()
# os.chdir('app/')

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

build_path = '~/Documents/git/mehemken.io/build/'
result = os.path.abspath(build_path)
FREEZER_DESTINATION = result


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    page = pages.get_or_404('about')
    return render_template('default.html', page=page)

if __name__ == '__main__':
    handler = RotatingFileHandler('logs/mehemken.io.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    args = parser.parse_args()

    if args.build:
        app.logger.info('Do you want to build?')
        ans = input('yes/no: ')
        if ans == 'yes':
            # freezer.freeze()
            app.logger.debug('This is where the build happens.')
        else:
            app.logger.info('build aborted')
    else:
        app.run(debug=True)
