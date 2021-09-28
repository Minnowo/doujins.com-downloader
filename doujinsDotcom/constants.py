import os 
import json
import tempfile

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

    
USER_AGENT = "Doujins.com command line client"

ILLEGAL_FILENAME_CHARS = "?*\"<>|"

BASE_URL = os.getenv('DOUJIN.COM', 'https://doujins.com')
LOGIN_URL = BASE_URL

u = urlparse(BASE_URL)
IMAGE_URL = '%s://static.%s/' % (u.scheme, u.hostname)

DOUJINS_HOME = os.path.join(os.getenv('HOME', tempfile.gettempdir()), '.doujins.com')
DOUJINS_CONFIG_FILE = os.path.join(DOUJINS_HOME, 'config.json')

CONFIG = {
    'proxy': {'http': '', 'https': ''},
    'cookie': '',
    'language': '',
    'truncate' : 100
}