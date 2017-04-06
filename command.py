#!/usr/bin/env python

import sys
import os
import logging

from app import freezer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('-b', '--build',
#         help='Build the static site.',
#         action='store_true')
# parser.add_argument('-p', '--path',
#         help='Print the build path.',
#         action='store_true')



if __name__ == '__main__':

    logger.info('foo bar baz')

#     args = parser.parse_args()
#
#     if args.path:
#         app.logger.info(FREEZER_DESTINATION)
#         sys.exit()
#
#     if args.build:
#         app.logger.info('Freezing the current site at\n{}'.format(FREEZER_DESTINATION))
#         try:
#             freezer.freeze()
#             app.logger.info('Freeze completed successfully.')
#         except:
#             app.logger.exception('There was an exception during the freeze.')
#         finally:
#             sys.exit('bye')
