# -*- coding: utf-8 -*-
# -
# Alice Nyaa
# https://github.com/Minnowo
# 2021-10-09
# -
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import re
import os.path
import warnings
from setuptools import setup, find_packages


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path, encoding="utf-8") as file:
        return file.read()

def check_file(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(path):
        return True
    warnings.warn(
        "Not including file '{}' since it is not present. "
        "Run 'make' to build all automatically generated files.".format(fname)
    )
    return False

with open('requirements.txt') as f:
    REQUIREMENTS = [l for l in f.read().splitlines() if l]

# get version without importing the package
VERSION = re.search(
    r'__version__\s*=\s*"([^"]+)"',
    read("doujinsDotcom/meta.py"),
).group(1)

LICENSE = re.search(
    r'__license__\s*=\s*"([^"]+)"',
    read("doujinsDotcom/meta.py"),
).group(1)

DESCRIPTION = ("Command-line program to download nhentai galleries")
LONG_DESCRIPTION = read("README.rst")



setup(
    name="doujinsDotcom",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/Minnowo/doujins.com-downloader",
    download_url="https://github.com/Minnowo/doujins.com-downloader",
    author="Alice Nyaa",
    author_email="",
    maintainer="Minnowo",
    maintainer_email="",
    include_package_data=True,
    license=LICENSE,
    python_requires=">=3.4",
    install_requires=REQUIREMENTS,
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "doujinsDotcom = doujinsDotcom:main",
        ],
    },
    keywords="image gallery downloader crawler scraper doujins hentai",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    test_suite="test"
)
