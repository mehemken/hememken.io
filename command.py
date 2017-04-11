#!/usr/bin/env python

import sys
import os
import logging
import subprocess

from app import freezer, FREEZER_DESTINATION

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-b', '--build',
        help='Build the static site.',
        action='store_true')
parser.add_argument('-p', '--path',
        help='Print the build path.',
        action='store_true')
parser.add_argument('-cd', '--commit_to_devel',
        help='Commit latest changes to build/ devel branch.',
        action='store_true')
parser.add_argument('-t', '--test',
        help='This will run the test suite on the development branch of the\
        build repo. If all tests pass changes will be pushed to devel origin.',
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
    finally:
        sys.exit()


def commit_to_devel():
    """Commit all changes to devel branch"""

    def get_status():
        status_args = 'git status'.split()
        p1 = subprocess.call(status_args)

    target_dir = '/home/emilio/Documents/git/mehemken.io/build'
    clean_target_dir = os.path.abspath(target_dir)
    os.chdir(clean_target_dir)

    devel_args = 'git checkout devel'.split()
    p0 = subprocess.call(devel_args)

    # Add?
    get_status()
    response_1 = input('Add all? ([Y]es/[N]o/[E]xit) ')
    if response_1 == 'y':
        add_args = 'git add .'.split()
        p2 = subprocess.call(add_args)
        get_status()
    elif response_1 == 'e':
        logger.info('Exiting...')
        sys.exit()

    # Commit?
    get_status()
    response_2 = input('Commit all? ([Y]es/[N]o/[E]xit) ')
    if response_2 == 'y':
        commit_args = 'git commit -a'.split()
        p3 = subprocess.call(commit_args)
        get_status()
    elif response_2 == 'e':
        logger.info('Exiting...')
        sys.exit()

    # try:
    #     logger.info('Attempting...')
    # except:
    #     logger.exception('Fail...')
    #     sys.exit()
    # else:
    #     logger.info('Win...')
    # finally:
    #     logger.info('Exiting...')
    #     sys.exit()

if __name__ == '__main__':

    args = parser.parse_args()

    if args.test:
        run_tests()

    if args.commit_to_devel:
        logger.info('Committing changes to build/ devel branch...')
        commit_to_devel()

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
