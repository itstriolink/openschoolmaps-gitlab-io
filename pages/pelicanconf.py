#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'OpenSchoolMaps'
SITENAME = u'OpenSchoolMaps.ch'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['images', 'favicons', 'file-icons']
EXTRA_PATH_METADATA = {
    'favicons': {'path': ''},
}
OUTPUT_PATH = 'public'

# When adding plugins here, also adapt
# docker.build/Dockerfile.build to provide them
# in the resulting Docker image.
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['asciidoc_reader']

TIMEZONE = 'Europe/Zurich'

DEFAULT_LANG = u'de'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('OpenStreetMap-Wiki', 'https://wiki.openstreetmap.org/wiki/DE:Switzerland/Lehrmittel#OpenSchoolMaps'),
    ('GitLab', 'https://gitlab.com/openschoolmaps/openschoolmaps.gitlab.io'),
    ('Issue-Tracker', 'https://gitlab.com/openschoolmaps/openschoolmaps.gitlab.io/issues'),
)

# Social widget
SOCIAL = LINKS

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
