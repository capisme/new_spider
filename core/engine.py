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

    # ��������Ϣ�����
    async def start(self):
        # ������������
        self.load_scripets()
        # ��ȡ��������
        self._init_crawler_configs()
        # ���Ӷ���
        await self.sch.connect()

        for cfg in self.crawler_configs:
            # print(cfg)
            id_ = cfg['id']
            crawler = NewsCrawler(cfg)
            # ���id���ֵ�����������������
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

    # ������������
    def load_scripets(self):
        # scripts = os.listdir('D:/PyProject/Project/spider/scripts')
        scripts = os.listdir('D:/PyProject/Project/Project/spider/scripts')
        for script in scripts:
            if not script.endswith('.py') or script == '__init__.py':
                continue
            moudle = importlib.import_module(f'spider.scripts.{script.replace(".py", "")}')
            for _, v in moudle.__dict__.items():
                # ������������Ҫ��Special
                if type(v) == type and 'Special' in str(v):
                    # �� idΪ�� ��Ϊֵ
                    self.special_dict[v.spider_id] = v

    # ��ȡ��������
    def _init_crawler_configs(self, db='spider01', table='gov_sites_config'
                                                         ''):
        # �ж�һ���Ƿ����������ݿ�ͱ���
        if not db or not table:
            logger.error("�������ݿ�")
            return
        self.crawler_configs = CrawlerConfig().get_configs(db, table)
        # print('������ϢΪ:', self.crawler_configs)
        return self.crawler_configs


if __name__ == '__main__':
    e = Engineer()
    # e._init_crawler_configs()
    asyncio.run(e.start())
