# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/1/30 16:45
# @Author : Cap
# @File : schedule
# @Project : acqNewsyb
import asyncio
import aioredis
from settings import REDIS_CONFIG,CONCURRENCY_REQUEST_NUM
REDIS_CFG = {
    "address": f"redis://{REDIS_CONFIG.get('host')}:{REDIS_CONFIG.get('port')}",
    "db": REDIS_CONFIG.get('db'),
    'password': REDIS_CONFIG.get('password'),
    'encoding': 'utf-8',
    'timeout': 20,
}


class AioRedis:
    def __init__(self):
        self.redis_cli = None

    async def connect(self):
        if not self.redis_cli:
            self.redis_cli = await aioredis.create_redis_pool(**REDIS_CFG)
        return self.redis_cli

    async def pop_task(self, key):
        return await self.redis_cli.rpop(key)

    async def insert_task(self, key, value):
        await self.redis_cli.lpush(key, value)

    async def get_tasks(self, key):
        tasks = [asyncio.create_task(self.pop_task(key)) for _ in range(CONCURRENCY_REQUEST_NUM)]
        await asyncio.gather(*tasks)
        results = [task.result() for task in tasks if task.result() is not None]
        return results

