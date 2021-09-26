
import os
import json
import argparse
import sys

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from constants import ILLEGAL_FILENAME_CHARS, CONFIG, DOUJINS_HOME,DOUJINS_CONFIG_FILE
    from logger import logger
    from __init__ import __version__
except ImportError:
    from doujinsDotcom.constants import ILLEGAL_FILENAME_CHARS, CONFIG, DOUJINS_HOME, DOUJINS_CONFIG_FILE
    from doujinsDotcom.logger import logger
    from doujinsDotcom.__init__ import __version__

def banner():
    logger.info(u'''Doujins.com ver %s: 
 _____                             
|     \  ___  _   _ _____ _        ____   
|  /\  |  _ \| | | |__   (_)_ __  /    \   ____  ___  __  __
| (  ) | / \ | | | |_ | || | `_ \|\  |_/  |   _|/ _ \/  \/  \  
|  \/  | \_/ | |_/ | \| || | | | |/\  \  _|  (_| |_| | |\/| |
|_____/ \___/ \__/\|\___/|_|_| |_|\___ /|_|____|\___/|_|  |_|

''' % __version__)

def load_config():
    if not os.path.exists(DOUJINS_CONFIG_FILE):
        return

    try:
        with open(DOUJINS_CONFIG_FILE, 'r') as f:
            CONFIG.update(json.load(f))

    except json.JSONDecodeError:
        logger.error('Failed to load config file.')
        write_config()


def write_config():
    if not os.path.exists(DOUJINS_CONFIG_FILE):
        os.mkdir(DOUJINS_CONFIG_FILE)

    with open(DOUJINS_CONFIG_FILE, 'w') as f:
        f.write(json.dumps(CONFIG))

def parse_args(args):
    
    parser = argparse.ArgumentParser(description='Doujins.com downloader')
    group = parser.add_mutually_exclusive_group()


    group.add_argument('-d', '--download', dest='download', action='store_true',
        help="download the doujinshi")

    group.add_argument('-I', '--info', dest='show_info', action='store_true',
        help="shows the info about the given doujin")

    group.add_argument('-sf', '--sauce-file', dest='sauce_file', action='store_true',
        help="generates an html file with all the images contained")

    group.add_argument('-m', '--meta-file', dest='meta_file', action='store_true',
        help="generates a .json file with the doujinshi metadata")


    parser.add_argument('-F', '--file', type=str, dest='doujin_ids_file', metavar='',
        help='reads doujin urls from a file, ( urls split by line )')

    parser.add_argument('-u', '--url', type=str, dest='urls', metavar='',
        help="specify the doujinshi urls")

    parser.add_argument('-f', '--format', type=str, dest='name_format', metavar='',
        help='specify the doujinshi folder name format.', default='%p')

    parser.add_argument('-o', '--output', type=str, dest='output', metavar='', default='downloads\\',
        help="specify the output directory")

    parser.add_argument('-sfo', '--sauce-file-output', type=str, dest='sauce_file_output', metavar='', default='%p.html',
        help="specify the output file of a sauce file")

    parser.add_argument('-t', '--threads', type=int, dest='threads', metavar='', default=5,
        help="specify the number of threads")

    parser.add_argument('-T', '--timeout', type=int, dest='timeout', metavar='', default=30,
        help='specify the request timeout')

    parser.add_argument('-D', '--delay', type=int, dest='delay', metavar='', default=0,
        help='set delay between downloads')

    parser.add_argument('-hf', '--html-format', dest='html_format', type=str, metavar='', default='default',
        help='the html template to use')

    parser.add_argument('-nh', '--no-html', dest='generate_html',  action='store_false',
        help='should an html viewer be created after downloading')

    parser.add_argument('-nm', '--no-meta', dest='generate_meta_file',  action='store_false',
        help='should the doujin meta be saved in a json file')



    parser.add_argument('-sp', '--set-proxy', type=str, dest='proxy', metavar='',
        help='store a proxy, for example: -p \'http://127.0.0.1:1080\'')

    parser.add_argument('-sc', '--set-cookie', type=str, dest='cookie', metavar='',
        help='set cookie of nhentai to bypass Google recaptcha')

    
    parser.add_argument('--cookie-help', action='store_true', dest='cookie_help',
        help='a guide on how to get and set your cookie')

    parser.add_argument('--format-help', action='store_true', dest='format_help',
        help='shows the different name formats')

    # Add login / cookie usage
    # Add search functionality


    args = parser.parse_args(args)
    
    if args.cookie_help:
        logger.info("To set your cookie use: --set-cookie \"YOUR COOKIE FROM doujins.com\"")
        logger.info("To get csrftoken and sessionid, first login to your doujin.com account, then:")
        logger.info("- Chrome  -> (Three dots)  -> More tools    -> Developer tools -> Application -> Storage -> Cookies -> https://doujins.com")
        logger.info("- Firefox -> (Three lines) -> Web Developer -> Developer tools -> Storage     -> Cookies -> https://doujins.com")
        sys.exit(0)

    if args.format_help:
        logger.info("formats are:")
        logger.info("\t%i : Doujin id")
        logger.info("\t%t : Doujin name")
        logger.info("\t%a : Doujin authors")
        sys.exit(0)

    if args.cookie is not None:
        CONFIG['cookie'] = args.cookie
        logger.info('Cookie saved.')
        write_config()
        sys.exit(0)

    if args.proxy is not None:
        proxy_url = urlparse(args.proxy)

        if not args.proxy == '' and proxy_url.scheme not in ('http', 'https'):
            logger.error("Invalid protocol '{0}' of proxy, ignored".format(proxy_url))
            sys.exit(1)

        CONFIG['proxy'] = {
            'http' : args.proxy,
            'https' : args.proxy
        }

        logger.info("Proxy now set to '{0}'.".format(args.proxy))
        write_config()
        sys.exit(0)

    if not args.download and not args.show_info and not args.sauce_file and not args.meta_file:
        logger.critical("No operation specified, use -h for help")
        sys.exit(1)

    if not args.urls and not args.doujin_ids_file:
        logger.critical("No doujinshi ids specified")
        sys.exit(1)

    elif args.urls:
        _ = [i.strip() for i in args.urls.split(',')]
        args.urls = set(str(i) for i in _ if i)

    else:
        with open(args.doujin_ids_file, 'r') as f:
            _ = [i.strip() for i in f.readlines()]
            args.urls = set(str(i) for i in _ if i)


    if args.output:
        has_c = args.output.find(":")
        if any([args.output.find(i) != -1 for i in ILLEGAL_FILENAME_CHARS] or (has_c != 1 and has_c != -1)):
            logger.critical("Output directory contains illegal characters")
            sys.exit(1)

    if args.name_format:
        has_c = args.output.find(":")
        if any([args.name_format.find(i) != -1 for i in ILLEGAL_FILENAME_CHARS] or (has_c != 1 and has_c != -1)):
            logger.critical("Name format contains illegal characters")
            sys.exit(1)

    if args.html_format not in ("default", "minimal"):
        logger.critical("Invalid html format")
        sys.exit(1)

    if args.threads < 0:
        args.threads = 1

    if args.delay < 0:
        args.delay = 0

    if args.timeout < 0:
        args.timeout = 0

    return args

