# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2022/11/27 22:37
# @Author : Cap
# @File : parse
# @Project : acq_news
from lxml import etree
from urllib.parse import urljoin
from gne import GeneralNewsExtractor
from utils.tools import fmt_pubtime

import utils.tools


class GeneralParser:

    def __init__(self, html):
        self.html = html
        self.xpathor = etree.HTML(html)
        self.gne = GeneralNewsExtractor()

    # 解析 a标签的url
    def parse_url(self, base, url_xpath=None):
        urls = []
        if url_xpath:
            hrefs = self.xpathor.xpath(url_xpath)
            for i in hrefs:
                # base 是板块的url url 是xpath的url
                url = urljoin(base=base, url=i)
                urls.append(url)
        return urls

    def parse_item(self, title_xpath=None, pubtime_xpath=None, contet_xpath=None):
        item = self.gne.extract(self.html)
        if title_xpath:
            title = self.parse_title(title_xpath)
        else:
            title = item['title']
        publish_time = self.publish_time() if pubtime_xpath else item['publish_time']
        content = self.content() if contet_xpath else item['content']
        return {
            'title': title,
            'publish_time': self.fmt_publish_time(publish_time),
            'content': content,
        }

    def parse_title(self, title_xpath):
        try:
            title = self.xpathor.xpath(title_xpath)[0]
            # print(title)
            return title
        except:
            return None

    @staticmethod
    def fmt_publish_time(data):
        return fmt_pubtime(data)

    def publish_time(self, publish_time_xpath):
        try:
            publish_time = self.xpathor.xpath(publish_time_xpath)[0]
            return publish_time
        except:
            return None

    def parse_content(self, content_xpath):
        try:
            content = self.xpathor.xpath(content_xpath)
            s = ''
            for c in content:
                s += c.xpath('string(.)')
            return s
        except:
            return None
