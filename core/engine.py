# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/2/14 1:02
# @Author : Cap
# @File : engine
# @Project : Project
import asyncio
import os
import importlib
from types import GeneratorType
from piplines.mysql_pipline import MysqlPipeline
from utils.json_code import *
import settings
from crawler_config import CrawlerConfig
from spider.newsSpider import NewsCrawler
from schedule import AioRedis
from download import Downloader
from utils.send_email import Email

logger = settings.logger


class Engineer:
    def __init__(self):
        self.crawler_configs = None
        self.sch = AioRedis()
        self.special_dict = {}
        self.email = Email()

    # 将请求信息入队列
    async def start(self):
        # 加载特殊爬虫
        self.load_scripets()
        # 获取配置数据
        self._init_crawler_configs()
        # 连接队列
        await self.sch.connect()

        for cfg in self.crawler_configs:
            # print(cfg)
            id_ = cfg['id']
            crawler = NewsCrawler(cfg)
            # 如果id在字典里面则是特殊爬虫
            if id_ in self.special_dict:
                crawler = self.special_dict[id_](cfg)
            request_ = crawler.start_request()
            if type(request_) == GeneratorType:
                for req in request_:
                    await self.sch.insert_task('queue', json_encode(req))
        await Downloader(self.sch).execute()

        update_sql = 'SELECT COUNT(*) FROM news_info WHERE DATE(inster_time)=CURDATE();'
        num = MysqlPipeline('spider01').select(sql=update_sql)
        update_num = (num[0][0])
        self.email.send_email(update_num)

    # 加载特殊爬虫
    def load_scripets(self):
        # scripts = os.listdir('D:/PyProject/Project/spider/scripts')
        scripts = os.listdir('D:/PyProject/Project/Project/spider/scripts')
        for script in scripts:
            if not script.endswith('.py') or script == '__init__.py':
                continue
            moudle = importlib.import_module(f'spider.scripts.{script.replace(".py", "")}')
            for _, v in moudle.__dict__.items():
                # 特殊爬虫类名要加Special
                if type(v) == type and 'Special' in str(v):
                    # 以 id为键 类为值
                    self.special_dict[v.spider_id] = v

    # 获取配置数据
    def _init_crawler_configs(self, db='spider01', table='gov_sites_config'
                                                         ''):
        # 判断一下是否有输入数据库和表名
        if not db or not table:
            logger.error("配置数据库")
            return
        self.crawler_configs = CrawlerConfig().get_configs(db, table)
        # print('配置信息为:', self.crawler_configs)
        return self.crawler_configs


if __name__ == '__main__':
    e = Engineer()
    # e._init_crawler_configs()
    asyncio.run(e.start())
