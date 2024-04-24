# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/1/29 16:50
# @Author : Cap
# @File : hns_gov_yaowen
# @Project : acqNewsyb
from spider.newsSpider import NewsCrawler
from spider.request import NewsRequest


class HnGovYwSpecialCrawler(NewsCrawler):
    spider_id = 1

    def start_request(self):
        url = self.config['section_url']
        # print(url)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        yield NewsRequest(url=url, headers=headers, callback=self.parse, request_type=1)
