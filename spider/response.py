# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/2/15 17:57
# @Author : Cap
# @File : response
# @Project : Project
import json


class Response:
    def __init__(self, content, url, headers, callback, status_code):
        self.content = content
        self.url = url
        self.headers = headers
        self.callback = callback
        self.status_code = status_code

        # self.cookies = cookies

    def json(self):
        return json.loads('')
