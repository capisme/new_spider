# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/2/14 13:48
# @Author : Cap
# @File : download
# @Project : Project
import asyncio
from types import GeneratorType
from item import NewsItem
from settings import logger
from spider.newsSpider import BaseCrawler
from utils.json_code import json_decode, json_encode
from pyppeteer import launch
from piplines.mysql_pipline import MysqlPipeline
from utils.send_email import Email

class Downloader:
    def __init__(self, sch):
        self.scheduler = sch
        self.email = Email()
    # ��ȡ�����ϵ�����
    async def execute(self):
        while True:
            request_tasks = await self.scheduler.get_tasks('queue')
            if not request_tasks:
                print('����Ϊ�� �˳�����')
                break
            await self.download(request_tasks)

    async def download(self, request_tasks):
        tasks = []
        # ����ֻ��һ�������
        browser = None
        # ��ȡ���г���
        sempahore = asyncio.Semaphore(len(request_tasks))
        for req in request_tasks:
            # ���� �������ض���
            req = json_decode(req)
            # print(req.request_type)
            # �ж���������� �����0 ������ͨ���� ������chrome �Զ���
            if req.request_type == 0:
                task = asyncio.create_task(BaseCrawler.request(sempahore, req))
            else:
                if browser is None:
                    browser = await launch(headless=False,
                                           args=[
                                               '--start-maximized',
                                               # f'--proxy-server={proxy}',
                                               '--disable-gpu',
                                               '--no-first-run',
                                               '--disable-dev-shm-usage',
                                               '--no-sandbox',
                                           ],
                                           handleSIGINT=False,
                                           handleSIGTERM=False,
                                           handleSIGHUP=False,
                                           # dumpio=True,
                                           ignoreDefaultArgs=['--enable-automation'], )
                task = asyncio.create_task(BaseCrawler.chrome_request(sema=sempahore, request=req, browser=browser))
            # task.add_done_callback(self.process_response)
            tasks.append(task)
        await asyncio.gather(*tasks)
        if browser:
            await browser.close()
        await self.process_response(tasks)

    async def process_response(self, response_tasks):
        for tsk in response_tasks:
            response = tsk.result()
            callback = response.callback
            try:
                callback_result = callback(response)
                if type(callback_result) == GeneratorType:
                    for r in callback_result:
                        await self.scheduler.insert_task('queue', json_encode(r))
                        print('���������',r.url)
                else:
                    # ���
                    clean_item=NewsItem(callback_result).field()
                    MysqlPipeline('spider01').insert('news_info',clean_item)
            except Exception as e:
                logger.error(f'����ʧ��- {response.url} - {e}')
