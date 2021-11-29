# log.py
# sets up logging format for the app to be used across.

import sys
import logging

INFO_FORMAT = '[%(asctime)s %(module)s.%(funcName)s:%(lineno)d] %(message)s'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger('API')
LOG.propagate = 0


def setup_handlers(logger):
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(INFO_FORMAT, TIMESTAMP_FORMAT)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


setup_handlers(LOG)


def get_logger():
    return LOG
