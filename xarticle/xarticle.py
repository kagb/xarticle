# -*-coding: utf-8 -*-

from urlparse import urlparse

from lxml.html import document_fromstring
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sitemap import SITE_MAP

TIME_OUT = 3


class XArticle(object):

    def __init__(self):
        self.fetcher = None
        self.site_conf = {}
        self.url = ''
        self.title = []
        self.summary = []
        self.pics = []
        self.videos = []
        if self.fetcher:
            self.fetcher.clear()
        else:
            self.fetcher = XFetcher()

    def extract(self, url):
        self.fetch(url)
        self.do_extract()

    def fetch(self, url):
        self.url = url
        self.fetcher.fetch(self.url, check_xpath=self.site_conf.get('check_xpath', ''))
        self.html = self.fetcher.html
        self.doc = self.fetcher.doc

    def do_extract(self):
        if self.doc is None:
            return
        parsed_url = urlparse(self.url)
        hostname = parsed_url.hostname
        default_conf = SITE_MAP.get(hostname, {})
        if not default_conf:
            default_conf = SITE_MAP['default']

        if not self.site_conf:
            self.site_conf = default_conf
        fields = self.site_conf.keys()

        for field in fields:
            setattr(self, field, None)
            _xpaths = self.site_conf.get(field, [])
            _xpaths = [_xpaths] if isinstance(_xpaths, str) else _xpaths
            for _xpath in _xpaths:
                result = []
                if not _xpath:
                    continue
                elements = self.doc.xpath(_xpath)
                if not elements:
                    continue
                if isinstance(elements, list):
                    result.extend(elements)
                else:
                    result.append(elements)
                result = list(set(result))
                setattr(self, field, result)

    def clear(self):
        return self.__init__()

    def quit(self):
        if self.fetcher:
            self.fetcher.quit()


class XFetcher(object):

    def __init__(self):
        self.url = ''
        self.browser = None
        self.html = ''
        self.doc = None

    def fetch(self, url, check_xpath='', timeout=TIME_OUT):
        self.url = url
        if not self.browser:
            self.browser = webdriver.PhantomJS()
        self.browser.get(url)
        try:
            if check_xpath:
                check_page = EC.presence_of_element_located((By.XPATH, check_xpath))
            else:
                def check_page(driver):
                    return driver.execute_script("return document.readyState") == "complete"
            WebDriverWait(self.browser, timeout).until(check_page)
        except TimeoutException:
            print "Warning: fetch web page timeout!"
        self.html = self.browser.page_source
        self.doc = document_fromstring(self.html)

    def clear(self):
        return self.__init__()

    def quit(self):
        if self.browser:
            self.browser.quit()
