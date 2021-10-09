# -*- coding: utf-8 -*-
# -
# Alice Nyaa
# https://github.com/Minnowo
# 2021-10-09
# -
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import os 
import tempfile

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

    
USER_AGENT = "Doujins.com command line client"

ILLEGAL_FILENAME_CHARS = "?*\"<>|"

BASE_URL = os.getenv('DOUJIN.COM', 'https://doujins.com')

DOUJINS_HOME = os.path.join(os.getenv('HOME', tempfile.gettempdir()), '.doujins.com')
DOUJINS_CONFIG_FILE = os.path.join(DOUJINS_HOME, 'config.json')

CONFIG = {
    'proxy': {'http': '', 'https': ''},
    'cookie': '',
    'language': '',
    'truncate' : 100
}