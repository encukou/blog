#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Petr Viktorin'
SITENAME = u"encukou/blog"
SITEURL = ''

TIMEZONE = 'Europe/Prague'

DEFAULT_LANG = u'en'

DELETE_OUTPUT_DIRECTORY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = False

RELATIVE_URLS = True

THEME = "theme/eck"

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<lang>[a-z]+)-(?P<slug>.*)'

DEFAULT_DATE_FORMAT = '%Y-%m-%d'
SITESUBTITLE = 'primary colors underneath'
FOOTER_TEXT = """
    powered by <a href="http://getpelican.com/">Pelican</a>
    <br>
    theme adapted from <a href="https://github.com/tbunnyman/pelican-chunk">pelican-chunk</a>
        by <a href="https://twitter.com/thisistran">Tran</a>
        and <a href="http://bunnyman.info/">tBunnyMan</a>
    <br>
    fonts: Signika by <a href="https://plus.google.com/u/0/105016556070324621004/about">Anna Giedryś</a>
        and Jockey One by <a href="https://plus.google.com/u/0/109781094858738402812/posts">TypeTogether</a>
    <br>
    fork this blog on <a href="https://github.com/encukou/github">Github</a>
    <br>
    <br>
    the text on this page is licensed under the
    <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
            Creative Commons Attribution-ShareAlike 3.0 Unported License</a>
    <br>
    by Petr Viktorin, <a href="http://encukou.cz">encukou.cz</a>
    """
DISPLAY_CATEGORIES_ON_MENU = False
SINGLE_AUTHOR = True
MENUITEMS_COLORFUL = (
        ('e-mail', 'mailto:encukou@gmail.com', '_kou'),
        ('github', 'http://github.com/encukou', '_cu'),
        ('twitter', 'https://twitter.com/encukou', '_en'),
    )
MENUITEMS = (
        ('home', 'http://encukou.cz'),
    )
XMENUITEMS = (
        ('blog', 'http://encukou.cz/blog'),
    )
DISPLAY_PAGES_ON_MENU = False

STATIC_PATHS = ['../images']

PAGE_DIR = '../pages'
FILES_TO_COPY = (('../extra/CNAME', 'CNAME'),)

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{lang}-{slug}'
ARTICLE_SAVE_AS = ARTICLE_URL + '/index.html'

ARTICLE_LANG_URL = ARTICLE_URL
ARTICLE_LANG_SAVE_AS = ARTICLE_SAVE_AS

YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL

CATEGORY_URL = 'blog/category/{slug}'
CATEGORY_SAVE_AS = CATEGORY_URL + '/index.html'

TAG_URL = 'blog/tag/{slug}'
TAG_SAVE_AS = TAG_URL + '/index.html'

DIRECT_TEMPLATES = ('siteindex', 'index', 'tags', 'categories', 'archives')
SITEINDEX_URL = 'encukou.cz'
SITEINDEX_SAVE_AS = 'index.html'
INDEX_URL = 'blog'
INDEX_SAVE_AS = INDEX_URL + '/index.html'
TAGS_URL = 'blog/tag'
TAGS_SAVE_AS = TAGS_URL + '/index.html'
CATEGORIES_URL = 'blog/category'
CATEGORIES_SAVE_AS = CATEGORIES_URL + '/index.html'
ARCHIVES_URL = 'blog/archive'
ARCHIVES_SAVE_AS = ARCHIVES_URL + '/index.html'

DEFAULT_LANG = "don't have one"
