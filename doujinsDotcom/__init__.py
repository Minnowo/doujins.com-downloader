# -*- coding: utf-8 -*-
# -
# Alice Nyaa
# https://github.com/Minnowo
# 2021-10-09
# -
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import sys
import os.path
from time import sleep
from signal import signal, SIGINT
from multiprocessing import freeze_support

from . import util
from . import cmdline
from .logger import logger
from .downloader import Downloader
from .constants import CONFIG
from .meta import __version__


def banner():
    logger.info(u'''Doujins.com ver %s: 
 _____                             
|     \  ___  _   _ _____ _          
|  /\  |  _ \| | | |__   (_)_ ___  ____    ____  ___  __  __
| (  ) | / \ | | | |_ | || | `_  \/  __\  |   _|/ _ \/  \/  \  
|  \/  | \_/ | |_/ | \| || | | | |/\_  \ _|  (_| |_| | |\/| |
|_____/ \___/ \__/\|\___/|_|_| |_|\___ /|_|____|\___/|_|  |_|

''' % __version__)


def main():

    signal(SIGINT, util.signal_handler)
    freeze_support()

    banner()

    downl = Downloader()
    
    args = cmdline.parse_args(sys.argv[1:])

    if args.gen_main:
        util.generate_main_html(args.output)
        return

    if CONFIG['proxy']['http']:
        logger.info('Using proxy: {0}'.format(CONFIG['proxy']['http']))

    downl.delay = args.delay
    downl.timeout = args.timeout
    downl.size = args.threads
    downl.path = args.output

    doujinshi = []
    for url in args.urls:
        logger.info("Fetching page for {}".format(url))
        d = Downloader.get_douijinshi(url)
        d.update_name_format(args.name_format)
        doujinshi.append(d)

    if args.meta_file:
        for d in doujinshi:

            if args.delay != 0:
                sleep(args.delay) 
            
            util.serialize_doujinshi(d, args.output, d.formated_name + ".metadata.json")

    elif args.sauce_file:
        for d in doujinshi:

            if args.delay != 0:
                sleep(args.delay) 

            util.generate_html_viewer_(args.output, util.format_doujin_string_(d, args.sauce_file_output), d, args.html_format, args.generate_meta_file, True) 

    elif args.download:

        for d in doujinshi:

            if args.delay != 0:
                sleep(args.delay) 

            d.downloader = downl
            d.download()
            d.download()
            
            if args.generate_html:
                util.generate_html_viewer_(os.path.join(args.output, d.formated_name), "index.html", d, args.html_format, args.generate_meta_file, False)

            elif args.generate_meta_file:
                util.serialize_doujinshi(d, args.output)

    else:
        for d in doujinshi:

            logger.info(str(d) + "\n") 


    logger.info('All done.')
