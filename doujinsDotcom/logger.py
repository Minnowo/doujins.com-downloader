# -*- coding: utf-8 -*-
# -
# Alice Nyaa
# https://github.com/Minnowo
# 2021-10-09
# -
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import logging
import sys


logger = logging.getLogger('doujinDotcom')

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
LOGGER_HANDLER.setFormatter(FORMATTER)

logger.addHandler(LOGGER_HANDLER)
logger.setLevel(logging.DEBUG)
