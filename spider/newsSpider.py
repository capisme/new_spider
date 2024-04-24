# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/1/29 15:23
# @Author : Cap
# @File : newsSpider
# @Project : acqNewsyb
import aiohttp

from .parse import GeneralParser
from .request import NewsRequest
from .response import Response
import settings

logger = settings.logger


class BaseCrawler:
    proxy = None

    def __init__(self, config):
        self.config = config

    # ��������
    @classmethod
    async def request(cls, semaphore, request):
        # ����3��
        retry = 3
        while retry > 0:
            retry -= 1
            try:
                async with semaphore:
                    con = aiohttp.TCPConnector(verify_ssl=False)
                    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
                        content = await cls._session_request(session, request)
                        return Response(content=content, url=request.url, headers=request.headers,
                                        callback=request.callback,  status_code=200)
            except Exception as e:
                logger.error(f"{request.url} ��{3 - retry}������ʧ�� - {e}")
            return Response(content=None, url=request.url, headers=request.headers,
                            callback=None, status_code=404)

    # �Զ�������
    @classmethod
    async def chrome_request(cls, sema, request, browser):
        async with sema:
            # ����3��
            retry = 3
            while retry > 0:
                retry -= 1
            try:
                page = await browser.newPage()
                await page.goto(request.url, {'waitUntil': 'networkidle0'})
                content = await page.content()
                await page.close()
                return Response(content=content.encode('utf8'), url=request.url, headers=request.headers,
                                callback=request.callback, status_code=200,)
            except Exception as e:
                logger.error(f"{request.url} ��{3 - retry}������ʧ�� - {e}")
                return Response(content=None, url=request.url, headers=request.headers,
                                callback=None, status_code=404,)

    @classmethod
    async def _session_request(cls, session, request):
        async  with session.get(request.url, headers=request.headers, timeout=request.timeout) as resp:
            content = await resp.read()
            return content


class NewsCrawler(BaseCrawler):

    def start_request(self):
        url = self.config['section_url']
        # request_type = self.config['request_type']
        yield NewsRequest(url=url, callback=self.parse, )

    def parse(self, response):
        # ���ж�һ���ַ��ڱ���
        if self.config['charset'] == 'gbk':
            charset = 'gbk'
        else:
            charset = 'utf-8'
        # �õ���������
        # print(response.text)
        # ����a��ǩxpath
        html = response.content.decode(charset)
        a_xpath = self.config['url_xpath']
        urls = GeneralParser(html).parse_url(base=self.config['section_url'], url_xpath=a_xpath)
        # print(urls)
        for url in urls:
            yield NewsRequest(url=url, callback=self.parse_detail, proxy=self.proxy)

    def parse_detail(self, response):
        # ���ж�һ���ַ��ڱ���
        if self.config['charset'] == 'gbk':
            charset = 'gbk'
        else:
            charset = 'utf-8'
        # �õ���������
        # print(response.text)
        # ����a��ǩxpath
        html = response.content.decode(charset)
        item = GeneralParser(html).parse_item()
        item['url'] = response.url
        return item
