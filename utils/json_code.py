# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/1/30 15:57
# @Author : Cap
# @File : json_code
# @Project : acqNewsyb
import base64
import pickle


def json_encode(data):
    json_b = pickle.dumps(data)
    json_encode_res = base64.b64encode(json_b)
    return json_encode_res


def json_decode(b_data):
    b_json = base64.b64decode(b_data)
    json_decode_res = pickle.loads(b_json)
    return json_decode_res
