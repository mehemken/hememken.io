#!/usr/bin/env python

import sys
import os
import logging
import subprocess
import shlex
import argparse
import shutil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

try:
    from app import freezer, FREEZER_DESTINATION
except ImportError:
    logger.info('Please activate frozen-flask.')
    sys.exit()


parser = argparse.ArgumentParser()
parser.add_argument('-b', '--build',
        help='Build the static site.',
        action='store_true')
parser.add_argument('-p', '--path',
        help='Print the build path.',
        action='store_true')
parser.add_argument('-c', '--commit',
        help='Commit latest changes to build/ devel branch.',
        action='store_true')
parser.add_argument('-t', '--test',
        help='This will run the test suite on the development branch of the\
        build repo. If all tests pass changes will be pushed to devel origin.',
        action='store_true')
parser.add_argument('-p', '--test_and_push',
        help='Run the test suite and push to origin',
        action='store_true')


def run_tests():
    logger.info('Running the test suite...')

    target_dir = '/home/emilio/Documents/git/mehemken.io/build'
    clean_target_dir = os.path.abspath(target_dir)

    os.chdir(clean_target_dir)

    try:
        pytest_args = 'pytest -v'.split()
        subprocess.Popen(pytest_args)
    except:
        logger.exception('Could not run the tests')
    else:
        logger.info('Subprocess for tests started without a hitch...')


def get_status():
    status_args = 'git status'.split()
    p = subprocess.call(status_args)


def prompt(git_string, question_string):
    response = input('{} (y/n/e) '.format(question_string))
    if response == 'y':
        git_args = shlex.split(git_string)
        p = subprocess.call(git_args)
        return True
    else:
        logger.info('Exiting...')
        sys.exit()


def commit():
    """Commit all changes to devel branch"""
    target_dir = '/home/emilio/Documents/git/mehemken.io/build'
    clean_target_dir = os.path.abspath(target_dir)
    os.chdir(clean_target_dir)

    logger.info('Moving to devel...')
    devel_args = 'git checkout devel'.split()
    p0 = subprocess.call(devel_args)
    logger.info('Ready...')

    # Add?
    get_status()
    prompt('git add .', 'Add all?')

    # Commit?
    get_status()
    prompt('git commit -a', 'Commit all?')

    # Merge?
    result = prompt('git checkout master', 'Merge?')
    if result:
        merge_arg = 'git merge devel'.split()
        checkour_arg = 'git checkout devel'.split()
        m = subprocess.call(merge_arg)
        c = subprocess.call(checkour_arg)


def test_n_push():
    logger.info('Running tests...')
    run_tests()
    logger.info('Push to origin...')
    result = prompt('git checkout master', 'Push?')
    if result:
        push_arg = shlex.split('git push')
        checkour_arg = shlex.split('git checkout devel')
        p = subprocess.call(push_arg)
        c = subprocess.call(checkour_arg)


def get_resume():
    # this is not implemented yet, but
    # I'd like to add a command to pull
    # my resume automatically from
    # it's home in another directory.
    pass


if __name__ == '__main__':

    args = parser.parse_args()

    if args.test:
        run_tests()

    if args.commit:
        logger.info('Committing changes to build/ devel branch...')
        commit()

    if args.path:
        logger.info(FREEZER_DESTINATION)
        sys.exit()

    if args.build:
        logger.info('Freezing the current site at\n{}'.format(FREEZER_DESTINATION))
        try:
            freezer.freeze()
            logger.info('Freeze completed successfully.')
        except:
            logger.exception('There was an exception during the freeze.')
        finally:
            sys.exit('bye')

    if args.test_and_push:
        test_n_push()
