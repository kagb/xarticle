# -*-coding: utf-8 -*-

import chardet
import requests
from lxml.html import document_fromstring


class XArticle(object):

    def __init__(self):
        self.url = ''
        self.doc = None
        self.html = ''
        self.title = ''

    def xurl(self, url, headers={}):
        self.fetch(url, headers)
        self._x()

    def _x(self):
        if self.doc is None:
            return
        title = self.doc.xpath('//title[position()=1]/text()')
        self.title = title[0] if title else u'None Title'

    def fetch(self, url, headers={}, **kwargs):
        self.__init__()
        self.url = url
        content = self.req_content(url, headers=headers, **kwargs)
        self.html = self.decode_content(content)
        self.doc = document_fromstring(self.html)

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
