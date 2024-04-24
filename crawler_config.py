from piplines.mysql_pipline import MysqlPipeline


# 此方法用来将获取的数据放到字典里面去
def arrange_config(cfg):
    config_field = {'id': cfg[0], 'site_name': cfg[1], 'host': cfg[2], 'section_name': cfg[3], 'section_url': cfg[4],
                    'url_xpath': cfg[5], 'url_format': cfg[6], 'end_page': cfg[7],
                    'publish_time_xpath': cfg[8], 'content_xpath': cfg[9], 'meta': cfg[10],
                    'is_crawl': cfg[11], 'level': cfg[12], 'type': cfg[13], 'area': cfg[14], 'charset': cfg[15], }
    return config_field


class CrawlerConfig:
    def column(self):
        pass

    # 此方法用来从库表获取配置信息
    def get_configs(self, db, table):
        config_field = {
            'id': 'id',  # 主键
            'site_name': 'site_name',  # 网站名
            'host': 'index',  # 网站首页
            'section_name': 'section_name',  # 板块名
            'section_url': 'section_url',  # 板块链接（起始请求的url）
            'url_xpath': 'url_xpath',  # 列表页解析的xpath
            'url_format': 'url_format',  # 用作翻页的格式化Url
            'end_page': 'end_page',  # 翻页所需的末尾页
            'title_xpath': 'title_xpath',  # 详情页标题xpath
            'publish_time_xpath': 'publish_time_xpath',  # 详情页发布时间xpath
            # 'author_xpath': 'author_xpath',  # 详情页作者xpath
            'content_xpath': 'content_xpath',  # 详情页内容xpath
            # 'step': 'step',  # 翻页所需的步长
            #  其他采集所需的配置信息
            'meta': 'meta',
            'is_crawl': 'is_crawl',
            'level': 'level',
            'type': 'type',
            'area': 'area',
            # {'url_reg': None, 'json_path': {}, 'list_title_xpath': None, 'list_pubtime_xpath': None}
            'charset': 'charset',
            # 'request_type':'request_type'
            # 'use_proxy': 'use_proxy',
            # 'crawl_freq': 'crawl_freq',
            # 'uniqueue_index': 'uniqueue_index',
            # 'update_time': 'update_time',

        }
        sql = f"select {','.join(['`{}`'.format(key) for key in config_field.values()])} from {table}"
        # print(sql)
        configs = MysqlPipeline(db).select(sql)
        # print(configs)
        configs_list = []
        for cfg in configs:
            configs_list.append(arrange_config(cfg))
        # print(configs_list)
        return configs_list


if __name__ == '__main__':
    cfg = CrawlerConfig()
    cfg.get_configs('spider01', 'config_copy1')