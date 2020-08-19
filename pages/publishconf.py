#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

_is_CI = 'CI' in os.environ

_official_url = 'https://openschoolmaps.ch'
_pages_url = os.getenv('CI_PAGES_URL', default='/')
_is_official_site = _pages_url == 'https://openschoolmaps.gitlab.io'
SITEURL = _official_url if _is_official_site else _pages_url
RELATIVE_URLS = not _is_CI

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# When switching to a different theme,
# adapt docker.build/Dockerfile.build
# to provide the theme files.
THEME = "pelican-themes/gum"

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
