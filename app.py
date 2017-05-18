#!/usr/bin/env python

import sys
import os
import logging

from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from flask import Flask, render_template, url_for, send_from_directory, redirect
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'pages'
BLOG_POSTS_DIR = 'posts'
DRAFT_POSTS_DIR = 'drafts'
build_path = '../build/files'
FREEZER_DESTINATION = build_path


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/about/')
def about():
    page = pages.get_or_404('index')
    resume = url_for('resume')
    return render_template('index.html', page=page, resume=resume)

@app.route('/')
def index():
    return redirect(url_for('blog'))

@app.route('/resume/')
def resume():
    resume = url_for('static', filename='resume/resume.pdf')
    return render_template('resume.html', resume=resume)

@app.route('/blog/')
def blog():
    posts = [p for p in pages if p.path.startswith(BLOG_POSTS_DIR)]
    posts.sort(key=lambda item:item['sortdate'], reverse=True)
    resume = url_for('resume')
    return render_template('posts.html', posts=posts, resume=resume)

@app.route('/blog/<name>/')
def blog_post(name):
    path = '{}/{}'.format(BLOG_POSTS_DIR, name)
    post = pages.get_or_404(path)
    resume = url_for('resume')
    return render_template('blog_post.html', post=post, resume=resume)

@freezer.register_generator
def blog_post():
    posts = [p for p in pages if p.path.startswith(BLOG_POSTS_DIR) ]
    for post in posts:
        yield {'name': post['slug']}

@app.route('/draft/<name>/')
def draft(name):
    path = '{}/{}'.format(DRAFT_POSTS_DIR, name)
    post = pages.get_or_404(path)
    resume = url_for('resume')
    return render_template('blog_post.html', post=post, resume=resume)

@freezer.register_generator
def draft():
    posts = [p for p in pages if p.path.startswith(DRAFT_POSTS_DIR) ]
    for post in posts:
        yield {'name': post['slug']}

@app.route('/static/css/pygments.css')
def pygments_css():
    return pygments_style_defs(style='tango'), 200, {'Content-Type': 'text/css'}

if __name__ == '__main__':
    handler = RotatingFileHandler('logs/mehemken.io.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(debug=True)
