#!/usr/bin/env python

import sys
import os
import logging

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
parser.add_argument('-c', '--commit',
        help='Commit latest changes to build master branch.',
        action='store_true')
parser.add_argument('-t', '--test',
        help='This will run the test suite on the development branch of the\
        build repo. If all tests pass changes will be pushed to devel origin.',
        action='store_true')



if __name__ == '__main__':

    args = parser.parse_args()

    if args.test:
        logger.info('This runs the test suite.')
        """
        Some code here.
        """

    if args.commit:
        logger.info('This commits all changes to build master.')
        """
        Some code here.
        """

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
