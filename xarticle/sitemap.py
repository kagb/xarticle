# -*- coding: utf-8 -*-

SITE_MAP = {
    'default': {
        'title': ['//title/text()'],
        'pics': ['//img/@src'],
        'videos': ['//video/@src'],
        'check_xpath': '',
    },
    'mp.weixin.qq.com': {
        'title': ['normalize-space(string(//h2[@class="rich_media_title"]))'],
        'pics': ['//div[@id="js_content"]//img/@data-src'],
        'videos': ['//div[@id="js_content"]//video/@src'],
        'check_xpath': '//div[@class="rich_media_content"]',
    },
    'm.weibo.cn': {
        'content': ['normalize-space(string(//p[contains(@class, "default-content")]))',
                    'normalize-space(string(//div[@class="weibo-og"]))',
                    ],
        'pics': ['//*[@class="weibo-detail"]//img/@src',
                 '//div[@class="weibo-og"]//img/@src',
                 ],
        'videos': ['//video/@src'],
        'check_xpath': '',
    },

}
