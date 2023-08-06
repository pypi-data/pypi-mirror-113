# -*- coding: utf-8 -*-

# author: 'ileona'
# date: 2021/7/12 11:32

from urllib.parse import urlencode
import time
import random


def splice_url(host, param):
    """
    拼接url地址
    :param host:
    :param param:
    :return:
    """
    return '?'.join([host.split('?')[0], urlencode(param)])


def parse_cookie(cookie, sep='; '):
    """
    将cookie字符串转为字典
    :param sep: 默认
    :param cookie:
    :return:
    """
    cookie_list = cookie.split(sep)
    cookie_dict = dict()
    for c in cookie_list:
        kv = c.split('=')
        cookie_dict[kv[0]] = '='.join(kv[1:])
    return cookie_dict


def random_time(a=2, b=5):
    """
    获取一个随机浮点数
    :param a: 最小值
    :param b: 最大值
    :return:
    """
    if a >= b:
        a, b = 2, 5
    return round(random.uniform(a, b), 2)

