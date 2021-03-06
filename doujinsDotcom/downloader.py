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
import requests

from re import search
from time import sleep
from signal import signal, SIGINT
from multiprocessing import Semaphore, Pool

from bs4 import BeautifulSoup

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from .logger import logger
from .constants import CONFIG
from .doujinshi import Doujinshi, DoujinshiInfo
from . import util

requests.packages.urllib3.disable_warnings()

semaphore = Semaphore(1)




class ImageNotExistsException(Exception):
    pass


class Downloader():

    def __init__(self, path='', size=5, timeout=30, delay=0):

        self.path = str(path)
        self.size = size
        self.timeout = timeout
        self.delay = delay

    def _download(self, url, folder='', filename='', retried=0, proxy=None):
        if self.delay:
            sleep(self.delay)

        filename = filename if filename else os.path.basename(urlparse(url).path)
        base_filename, extension = os.path.splitext(filename)
        output_filename = os.path.join(folder, base_filename.zfill(3) + extension)

        if os.path.exists(output_filename):
            logger.warning('File: {0} exists, ignoring'.format(output_filename))
            return 1, url
        
        logger.info('Starting to download {0} ...'.format(url))
        
        try:

            response = None

            with open(output_filename, "wb") as f:
                
                i = 0
                while i < 10:
                    try:
                        response = util.request_helper('get', url, stream=True, timeout=self.timeout, proxies=proxy)
                        if response.status_code != 200:
                            raise ImageNotExistsException

                    except ImageNotExistsException as e:
                        raise e

                    except Exception as e:
                        i += 1
                        if i >= 10:
                            logger.critical(str(e))
                            return 0, None
                        continue

                    break

                length = response.headers.get('content-length')
                if length is None:
                    f.write(response.content)
                else:
                    for chunk in response.iter_content(2048):
                        f.write(chunk)

        except (requests.HTTPError, requests.Timeout) as e:
            if retried < 3:
                return 0, self._Download(url=url, folder=folder, filename=filename, retried=retried+1, proxy=proxy)
            else:
                return 0, None

        except ImageNotExistsException as e:
            os.remove(os.path.join(folder, base_filename.zfill(3) + extension))
            return -1, url

        except Exception as e:
            logger.critical(str(e))
            return 0, None

        except KeyboardInterrupt:
            return -3, None

        return 1, url

    def download(self, queue, folder=''):
        """Start the download queue."""
        folder = str(folder)

        if self.path:
            folder = os.path.join(self.path, folder)

        if not os.path.exists(folder):
            logger.warning('Path \'{0}\' does not exist, creating.'.format(folder))
            if not util.create_directory(folder):
                logger.critical("Cannot create output folder, download canceled")
                return

        queue = [(self, url, folder, CONFIG['proxy'], str(index+1) + util.get_url_ext(url,True)) for index, url in enumerate(queue)]

        pool = Pool(self.size, _init_worker)
        [pool.apply_async(_download_wrapper, args=item) for item in queue]

        pool.close()
        pool.join()

        
        


    @staticmethod
    def get_douijinshi(url : str) -> Doujinshi:
        """Gets a Doujinshi object from doujins.com page source"""

        info = dict()

        doujin = Doujinshi()
        doujin.url = url

        page = Downloader.get_doujinshi_page(url)

        if not page:
            return doujin

        html = BeautifulSoup(page, 'html.parser')

        title_div = html.find('div', attrs={'class': 'folder-title'})

        _ = [i.text for i in title_div.find_all('a')]
        doujin.name = " - ".join(_)
        doujin.pretty_name = _[-1]
        
        tag_area = html.find('li', attrs={'class' : 'tag-area'})
        if tag_area:
            info['tags'] = ", ".join([i.text.strip() for i in tag_area.find_all('a') if i])

        else:
            info['tags'] = ""

        artists = html.find('div', attrs={'class' : 'gallery-artist'})
        if artists:
            info['artists'] = ", ".join([i.text.strip() for i in artists.find_all('a') if i])

        else:
            info['artists'] = ""

        message_area = html.find_all('div', attrs={'class':'folder-message'})
        if message_area:
            info['message'] = ", ".join([i.text.strip() for i in message_area if i])

        else:
            info['message'] = ""

        
        images_area = html.find_all('div', attrs={'class' : 'swiper-slide'})

        for slider in images_area:

            img = search(r'src=\"(.*?)\"', str(slider.find('img')))
            if img:
                page = img.group(1)
                
                # the urls look like this: https://static.doujins.com/n-ybqzb1dv.jpg?st=DIeNsEYQrnOyvHV1Y1D57g&e=1632413343
                # but when scraping from the page
                # they look like this    : https://static.doujins.com/n-ybqzb1dv.jpg?st=DIeNsEYQrnOyvHV1Y1D57g&amp;e=1632413343
                # and if they have the 'amp;' after the get request, the url doesn't work

                match = search(r'^(https|http)://static.doujins.com/(.*?)&(.*?);(.*?)$', page)
                
                if match:
                    # reformat the deconstructed url so that it doesn't contain the 'amp;' 
                    # only reason i'm not directly searching for 'amp;' is because i'm not sure 
                    # if its a constant for everything on the site, but chances are if its not
                    # the url will still have random characters before a ; after the get request
                    page = "{}://static.doujins.com/{}&{}".format(match.group(1), match.group(2), match.group(4))
                    
                doujin.pages.append(page)

        doujin.info = DoujinshiInfo(**info)
        doujin.update()

        return doujin
    
    @staticmethod
    def get_doujinshi_page(url : str) -> list:
        """Downloads the source of the given nhentai page and returns the contents as a byte[] or None."""

        try:
            response = util.request_helper('get', url)
            
            if response.status_code == 200:
                return response.content

            elif response.status_code == 404:
                logger.error("Doujinshi with url {0} cannot be found".format(url))
                return None

            else:
                logger.warning('Slow down and retry ({}) ...'.format(url))
                sleep(1)
                return Downloader.get_doujinshi_page(str(url))
        except:
            return None



def _download_wrapper(obj, url, folder='', proxy=None, filename=''):
    if sys.platform == 'darwin' or semaphore.get_value():
        return Downloader._download(obj, url=url, folder=folder, proxy=proxy, filename=filename)
    else:
        return -3, None
    


def _init_worker():
    signal(SIGINT, _subprocess_signal)


def _subprocess_signal(signal, frame):
    if semaphore.acquire(timeout=1):
        print('Ctrl-C pressed, exiting sub processes ...')

    raise KeyboardInterrupt




