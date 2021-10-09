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

if __package__ is None and not hasattr(sys, "frozen"):
    import os.path
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.realpath(path))


import doujinsDotcom

if __name__ == "__main__":
    sys.exit(doujinsDotcom.main())
