# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 10:34
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : c20_log_handler.py
# @Software: PyCharm

import json
import time
import pprint
from operator import itemgetter
from functools import reduce
from config.config import *
from hander.hander import Hander


class HanderC20(Hander):

    def __init__(self, path):
        self.path = path

    def compare(self, uri, url):
        if uri == url:
            return True
        url_params = url.split('/')
        uri_params = uri.split('/')
        comp_result = map(self.comp, uri_params, url_params)
        results = list(comp_result)

        result1 = reduce(lambda x, y: x and y, results)

        return result1

    def compare_url(self, uri, url):
        if uri == url:
            return True
        url_params = url.split('/')
        uri_params = uri.split('/')
        comp_result = map(self.comp, uri_params, url_params)
        results = list(comp_result)
        len1 = len(url_params)
        len2 = len(uri_params)

        result2 = False
        if len1 == len2 and len1 % 2 == 0 and len2 % 2 == 0:
            result_split = []
            i = 0
            while i < len(results):
                item = [results[i], results[i + 1]]
                result_split.append(item)
                i += 2

            n = 0
            rr = []
            while n < len(result_split):
                if result_split[n] == result_split[n + 1]:
                    rr.append(True)
                else:
                    rr.append(False)
                n += 2
            result2 = reduce(lambda x, y: x and y, rr)

        result1 = reduce(lambda x, y: x and y, results)

        return result1 or result2

    def comp(self, l1, l2):
        '''
        判断模板和url是否匹配
        :param l1:
        :param l2:
        :return:
        '''
        if l1 is None or l2 is None:
            return False

        if len(l1) == 0 and len(l2) == 0:
            return True

        if len(l1) == 0 or len(l2) == 0:
            return True

        if l1 == l2:
            return True

        if l1.startswith('{') and l1.endswith('}'):
            return True
        return False

    def is_same(self, u1, u2):
        '''
        判断2个url是否相同
        :param u1:
        :param u2:
        :return:
        '''
        if u1 == u2:
            return True
        f1 = u1.find('?')
        f2 = u2.find('?')
        if f1 > 0 and f2 > 0:
            u1s = u1.split('?')
            u2s = u2.split('?')
            if u1s[0] == u2s[0]:
                return True
        flag = self.compare(u1, u2)
        if flag:
            return flag
        return False

    def handle_url_doc(self, path):
        '''
        获取url模板
        :param path:
        :return:
        '''

        cfp = open(path, mode='r', encoding='utf-8')
        docs = []
        comments_dict = {}
        tpl_url = []
        for line in cfp.readlines():
            item = line.strip()
            item = item.strip('<?php')
            length = len(item)
            if length > 0:
                if item.startswith('//'):
                    i = item.strip('//')
                    comment = i.strip()
                    docs.append(comment)
                elif item.endswith(';'):
                    i = item.strip(';')
                    urls = i.split('=')
                    url = urls[1].strip().strip('\'')
                try:
                    if comment is not None and url is not None:
                        comments_dict[url] = comment
                        tpl_url.append(url)
                except:
                    pass
                finally:
                    pass

        tpl_urls = list(set(tpl_url))

        return tpl_urls, comments_dict

    def parse(self, path, tpl_urls, comments_dict):
        '''
        分析c20日志
        :param path:
        :param tpl_urls:
        :return:
        '''
        stat_url_dict = []
        fp = open(path, mode='r', encoding='utf-8')
        data = []
        for line in fp.readlines():
            line_content = line.split(',')
            try:
                if line_content and line_content[1]:
                    uri = line_content[1].replace('uri=[', '')
                    uri = uri.replace(']', '')
                    p = line_content.index('Content-Type=[application/json]')
                    options_arr = line_content[2:p]
                    str = ''.join(options_arr)
                    str = str.replace('headers=[Accept=[application/json]', '')
                    str = str.replace('options=[', '')
                    str = str.replace('json=[', '')
                    options = (str[:-1])
                    query = options.replace(']', '&')
                    query = query.replace('[', '')
                    option = (query.rstrip('&'))
                    options_params = option.split('&')
                    param_len = len(options_params)
                    options_params_arr = {}
                    if param_len > 0:
                        for i in options_params:
                            param = i.split('=')
                            options_params_arr.update({param[0]: param[1]})
                    if uri.startswith('http://192.168.10.67:8082'):
                        uri = uri.replace('http://192.168.10.67:8082', '')
                    elif uri.startswith('http://zsy.c20.org.cn:8082'):
                        uri = uri.replace('http://zsy.c20.org.cn:8082', '')
                    elif uri.startswith('http://192.168.10.64:8082'):
                        uri = uri.replace('http://192.168.10.64:8082', '')
                    elif uri.startswith('http://120.26.103.125'):
                        uri = uri.replace('http://120.26.103.125', '')
                    data.append({'uri': uri, 'param': options_params_arr})
            except:
                pass
            finally:
                pass
        fp.close()
        url_stat = {}
        for item in data:
            uri = item.get('uri', None)
            if uri is not None:
                for url in tpl_urls:
                    flag = self.is_same(url, uri)
                    if flag:
                        stat = url_stat.get(url)
                        if stat is not None:
                            url_stat[url] = stat + 1
                        else:
                            url_stat[url] = 1

        sort_stat = sorted(url_stat.items(), key=itemgetter(1), reverse=True)

        for u in sort_stat:
            item = {
                'url': u[0],
                'stat': u[1],
                'comment': comments_dict.get(u[0])
            }
            stat_url_dict.append(item)
        return stat_url_dict
