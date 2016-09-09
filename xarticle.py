# -*-coding: utf-8 -*-

import chardet
import requests
from urlparse import urlparse
from lxml.html import document_fromstring

from sitemap import SITE_MAP


class XArticle(object):

    def __init__(self):
        self.url = ''
        self.doc = None
        self.html = ''
        self.title = ''
        self.pic = ''
        self.pics = []
        self.videos = []

    def extract(self, url, headers={}):
        self.__init__()
        self.url = url
        parsed_url = urlparse(self.url)
        hostname = parsed_url.hostname
        site_conf = SITE_MAP.get(hostname, {})

        self.fetch(self.url, headers)
        self.do_extract(site_conf)

    def fetch(self, url, headers={}, **kwargs):
        content = self.req_content(url, headers=headers, **kwargs)
        self.html = self.decode_content(content)
        self.doc = self.html_to_doc(self.html)

    def do_extract(self, site_conf=SITE_MAP['default']):
        if self.doc is None:
            return
        default_conf = SITE_MAP['default']
        title_xpath = site_conf.get('title', default_conf['title'])
        pics_xpath = site_conf.get('pics', default_conf['pics'])
        videos_xpath = site_conf.get('videos', default_conf['videos'])

        title = self.doc.xpath(title_xpath)
        self.title = title[0] if title else u''

        self.pics = self.doc.xpath(pics_xpath)
        self.pic = self.pics[0] if self.pics else ''

        self.videos = self.doc.xpath(videos_xpath)

    @classmethod
    def req_content(cls, url, headers={}, timeout=10, verify=False, **kwargs):
        r = requests.get(url,
                         headers=headers,
                         timeout=timeout,
                         verify=verify,
                         **kwargs)
        content = r.content if r.status_code == 200 else ''
        return content

    @classmethod
    def decode_content(cls, content):
        encoding = 'utf-8'
        encoding_info = chardet.detect(content)
        if encoding_info.get('confidence', 0) > 0.9:
            encoding = encoding_info.get('encoding', 'utf-8')
        return content.decode(encoding, errors='replace')

    @classmethod
    def html_to_doc(cls, html):
        return document_fromstring(html)
