
import logging
import sys


logger = logging.getLogger('doujinDotcom')

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
LOGGER_HANDLER.setFormatter(FORMATTER)

logger.addHandler(LOGGER_HANDLER)
logger.setLevel(logging.DEBUG)
