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

from flask import Flask, render_template, url_for
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
    return render_template('index.html', page=page)

@app.route('/resume/')
def resume():
    page = pages.get_or_404('resume')
    resume = url_for('static', filename='resume/resume.pdf')
    return render_template('resume.html', page=page, resume=resume)


if __name__ == '__main__':
    handler = RotatingFileHandler('logs/mehemken.io.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    args = parser.parse_args()

    if args.path:
        app.logger.info(FREEZER_DESTINATION)
        sys.exit()

    if args.build:
        app.logger.info('Freezing the current site at\n{}'.format(FREEZER_DESTINATION))
        try:
            freezer.freeze()
            app.logger.info('Freeze completed successfully.')
        except:
            app.logger.exception('There was an exception during the freeze.')
        finally:
            sys.exit('bye')

    app.run(debug=True)
