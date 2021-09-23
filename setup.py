# coding: utf-8
from __future__ import print_function, unicode_literals
import sys
import codecs
from setuptools import setup, find_packages

try:
    from doujinsDotcom import __version__, __author__, __email__
except ImportError:
    from doujinsDotcom.__init__ import __version__, __author__, __email__

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]


def long_description():
    with codecs.open('README.rst', 'rb') as readme:
        if not sys.version_info < (3, 0, 0):
            return readme.read().decode('utf-8')


setup(
    name='doujinsDotcom',
    version=__version__,
    packages=find_packages(),

    author=__author__,
    author_email=__email__,
    keywords=['doujinshi', 'downloader'],
    description='doujins.com doujinshis downloader',
    long_description=long_description(),
    url='https://github.com/Minnowo/doujins.com-downloader',
    download_url='https://github.com/Minnowo/doujins.com-downloader',
    include_package_data=True,
    zip_safe=False,

    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'doujinsDotcom = doujinsDotcom.main:main',
        ]
    },
    license='GPL-3.0',
)
