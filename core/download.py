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
    # 获取队列上的任务
    async def execute(self):
        while True:
            request_tasks = await self.scheduler.get_tasks('queue')
            if not request_tasks:
                print('队列为空 退出任务')
                break
            await self.download(request_tasks)

    async def download(self, request_tasks):
        tasks = []
        # 控制只有一个浏览器
        browser = None
        # 获取队列长度
        sempahore = asyncio.Semaphore(len(request_tasks))
        for req in request_tasks:
            # 解码 将编码变回对象
            req = json_decode(req)
            # print(req.request_type)
            # 判断请求的类型 如果是0 就用普通请求 否则用chrome 自动化
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
                        print('重新入队列',r.url)
                else:
                    # 入库
                    clean_item=NewsItem(callback_result).field()
                    MysqlPipeline('spider01').insert('news_info',clean_item)
            except Exception as e:
                logger.error(f'解析失败- {response.url} - {e}')
