import loguru, datetime

PROJECT_NAME = 'acq-news'

logger = loguru.logger
day = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
logger.add(
    sink=f'logs/{day}.log',
    level='INFO',
    enqueue=True,  # 异步
    encoding='utf-8',
)

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "root",
    "db": "spider",
    "port": 3306,
    "charset": "utf8",
}

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 1,
    "decode_responses": True,
    'password': 'root',
    'bloom_key':'news_bloom_filter'
}

CONCURRENCY_REQUEST_NUM = 50

DOWNLOAD_QUEUE_NAME =''