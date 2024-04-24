import re

from utils.tools import get_md5


class NewsItem:
    def __init__(self, item):
        self.item = item

    def field(self):
        for k in self.item:
            if type(self.item[k]) is str:
                self.item[k] = self.clean_data(self.item[k])
        self.item['url_md5'] = get_md5(self.item['url'])
        return self.item

    def check(self):
        print('检测标题、时间、内容、url这些关键字段是否为空，如果为空不能入库')
        if self.item['title'] == None:
            pass

    def clean_data(self, data: str):
        # 去除特殊字符
        news = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', "", data)
        # 将中文符号替换为英文符号
        news = news.replace('，', ',').replace('。', '.').replace('！', '!').replace('？', '?')
        # 将大写字母转换为小写
        news = news.lower()
        # 返回清洗后的新闻
        return news
