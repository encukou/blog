#!/usr/bin/env python

import markdown
import re
import os

from pelican import signals

AUTHOR = u'Petr Viktorin'
SITENAME = u"encukou/blog"
SITEURL = ''

TIMEZONE = 'Europe/Prague'

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

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<day_disambig>\d+-)?(?P<lang>[a-z]+)-(?P<slug>.*)'

DEFAULT_DATE_FORMAT = '%Y-%m-%d'
SITESUBTITLE = 'primary colors underneath'
FOOTER_TEXT = """
    powered by <a href="http://getpelican.com/">Pelican</a>
    <br>
    theme adapted from <a href="https://github.com/tbunnyman/pelican-chunk">pelican-chunk</a>
        by <a href="https://twitter.com/thisistran">Tran</a>
        and <a href="http://bunnyman.info/">tBunnyMan</a>
    <br>
    fonts: Signika by <a href="http://ancymonic.com/">Anna Giedryś</a>
        and Jockey One by <a href="www.type-together.com">TypeTogether</a>
    <br>
    fork this blog on <a href="https://github.com/encukou/blog">Github</a>
    <br>
    <br>
    the text on this page is licensed under the
    <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
            Creative Commons Attribution-ShareAlike 3.0 Unported License</a>
    <br>
    by Petr Viktorin, <a href="http://encukou.cz">encukou.cz</a>
    """
FOOTER_TEXT_CS = """
    tento blog používá systém <a href="http://getpelican.com/">Pelican</a>
    <br>
    styl adaptovaný z <a href="https://github.com/tbunnyman/pelican-chunk">pelican-chunk</a>
        © <a href="https://twitter.com/thisistran">Tran</a>
        a <a href="http://bunnyman.info/">tBunnyMan</a>
    <br>
    použité fonty: Signika © <a href="http://ancymonic.com/">Anna Giedryś</a>
        a Jockey One © <a href="www.type-together.com">TypeTogether</a>
    <br>
    tento blog je na <a href="https://github.com/encukou/blog">Githubu</a>
    <br>
    <br>
    text na této stránce je k dispozici pod licencí
    <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
            Creative Commons Attribution-ShareAlike 3.0 Unported</a>
    <br>
    © Petr Viktorin, <a href="http://encukou.cz">encukou.cz</a>
    """
DISPLAY_CATEGORIES_ON_MENU = False
SINGLE_AUTHOR = True
MENUITEMS_COLORFUL = (
        ('e-mail', 'mailto:encukou@gmail.com', '_kou'),
        ('twitter', 'https://twitter.com/encukou', '_cu'),
        ('github', 'http://github.com/encukou', '_en'),
    )
MENUITEMS = (
        ('home', 'http://encukou.cz'),
    )
XMENUITEMS = (
        ('blog', 'http://encukou.cz/blog'),
    )
DISPLAY_PAGES_ON_MENU = False

PAGE_PATHS = ['pages']
STATIC_PATHS = [
    '../images',
    '../extra/CNAME',
    ]
STATIC_SAVE_AS = 'output/{path}'
EXTRA_PATH_METADATA = {
    '../extra/CNAME': {'path': '../CNAME'},
    }

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{lang}-{slug}'
ARTICLE_SAVE_AS = ARTICLE_URL + '/index.html'

ARTICLE_LANG_URL = ARTICLE_URL
ARTICLE_LANG_SAVE_AS = ARTICLE_SAVE_AS

YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/index.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL

CATEGORY_URL = 'blog/category/{slug}'
CATEGORY_SAVE_AS = CATEGORY_URL + '/index.html'

TAG_URL = 'blog/tag/{slug}'
TAG_SAVE_AS = TAG_URL + '/index.html'

DIRECT_TEMPLATES = (
    'siteindex', 'index', 'tags', 'categories', 'archives', 'period_archives',
)
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

SUMMARY_MAX_LENGTH = None


# Join one-letter words (Czech typography convention)

class VlnaExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('vlna', VlnaProcessor(), '_begin')

class VlnaProcessor(markdown.treeprocessors.Treeprocessor):
    def fix(self, text):
        previous = text
        text = re.sub(r'\b([ksvzouiaKSVZOUIA]) (\w)', r'\1&nbsp;\2', text)  # k oknu
        text = re.sub(r'(\d) (\d)', r'\1&nbsp;\2', text)  # 4 500
        text = re.sub(r'(\d\.?) (\w)', r'\1&nbsp;\2', text)  # 10 kg
        text = re.sub(r'(\d\.) (\d)', r'\1&nbsp;\2', text)  # 2. 4.
        text = re.sub(r'(.{30}) ([^ &]+[.?!])$', r'\1&nbsp;\2', text)  # last word
        if previous != text:
            return self.fix(text)
        return text

    def run(self, node):
        if node.tag in ('pre', 'code'):
            return node
        if node.text:
            node.text = self.fix(node.text)
        for child in node.getchildren():
            self.run(child)
        return node

class GithubLinkPlugin(object):
    __name__ = 'GithubLinkPlugin'
    def add_github_links(self, generator):
        for article in generator.articles:
            article.github_url = GITHUB_URL + os.path.relpath(article.source_path, '.')

    def register(self):
        signals.article_generator_finalized.connect(self.add_github_links)

MARKDOWN = {
    'extensions': [
        'codehilite',
        'extra',
        'mdx_headdown',
        'toc',
        VlnaExtension(),
    ],
    'extension_configs': {
        'codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
        },
        'mdx_headdown': {
            'offset': 1,
        }
    },
}

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['summary', 'neighbors', 'latex', GithubLinkPlugin()]

GITHUB_URL = 'https://github.com/encukou/blog/blob/master/'

SITEURL = 'http://encukou.cz'
