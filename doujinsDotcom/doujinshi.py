
import datetime

try:
    from constants import BASE_URL
    from logger import logger
    from helpers import format_filename
except ImportError:
    from doujinsDotcom.constants import BASE_URL
    from doujinsDotcom.logger import logger
    from doujinsDotcom.helpers import format_filename

class DoujinshiInfo(dict):
    def __init__(self, **kwargs):
        super(DoujinshiInfo, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return ''


class Doujinshi(object):
    def __init__(self, url="", name="", pretty_name="",
    name_format='%i', downloader=None, **kwargs):

        self.url = url

        self.name = name
        self.pretty_name = pretty_name
        self.name_format = name_format

        self.pages = [] # forgot that python defines function defaults at runtime, this NEEDS to be here not in the __init__
        self.page_count = len(self.pages)
        self.downloader = downloader
        self.info = DoujinshiInfo(**kwargs)

        _name_format = name_format.replace('%a', self.info.artists)
        _name_format = _name_format.replace('%t', self.name)
        _name_format = _name_format.replace('%p', self.pretty_name)
        self.formated_name = format_filename(_name_format)

        self.table = [
            ["URL", self.url],
            ["Doujinshi", self.name],
            ["Authors", self.info.artists],
            ["Tags", self.info.tags],
            ["Message", self.info.message],
            ["Pages", self.pages]
        ]


    def update_name_format(self, new_name_format):
        """Updates the name format, and the formated name."""
        self.name_format = new_name_format
        _name_format = new_name_format.replace('%a', self.info.artists)
        _name_format = _name_format.replace('%t', self.name)
        _name_format = _name_format.replace('%p', self.pretty_name)
        self.formated_name = format_filename(_name_format)


    def update(self):
        """Updates the page count, url, and table."""
        self.page_count = len(self.pages)
        self.table = [
            ["URL", self.url],
            ["Doujinshi", self.name],
            ["Authors", self.info.artists],
            ["Tags", self.info.tags],
            ["Message", self.info.message],
            ["Pages", self.pages]
        ]

    
    def download(self):
        """Begin downloading the doujin."""

        logger.info('Starting to download doujinshi: %s' % self.name)

        if not self.downloader:
            logger.error("No downloader has been loaded, cannot download.")
            return

        if self.page_count < 1:
            logger.error("Doujin object has no defined pages.")
            return

        download_queue = []
        for i in self.pages:
            download_queue.append(i)

        self.downloader.download(download_queue, self.formated_name)



    def __repr__(self):

        out = """Doujinshi information of %s
----------  ------------------------------------------------------------------------
Doujinshi   %s
Authors     %s
Pages       %d
Tags        %s
Messages    %s
----------  ------------------------------------------------------------------------""" % (self.url, self.name, 
        self.info.artists, self.page_count, self.info.tags, self.info.message)

        return out