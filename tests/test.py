# -*- coding: utf-8 -*-
# @Time    : 2019/9/29 15:26
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : etest.py
# @Software: PyCharm
import re
import operator
from functools import reduce


def compare_url(uri,url):
    if uri == url:
        return True
    url_params = url.split('/')
    uri_params = uri.split('/')
    comp_result = map(comp, uri_params, url_params)
    results = list(comp_result)
    result_split = []
    i = 0

    while i< len(results):
        item = [results[i], results[i+1]]
        result_split.append(item)
        i += 2
    n = 0

    rr = []
    while n < len(result_split):
        if result_split[n] == result_split[n+1]:
            rr.append(True)
        else:
            rr.append(False)
        n += 2

    result1 = reduce(lambda x, y: x and y, results)
    result2 = reduce(lambda x, y: x and y, rr)

    return result1 or result2

def comp(l1, l2):

    if l1 is None or l2 is None:
        return False

    if len(l1)== 0 and len(l2) == 0:
        return True

    if len(l1)== 0 or len(l2) == 0:
        return True

    if l1 == l2:
        return True

    if l1.startswith('{') and l1.endswith('}'):
        return True
    if l2.startswith('{') and l2.endswith('}'):
        return True

    return False


uri = '/api/analysis/base/situation/0df0e162-8660-46dd-94d0/space/3'
url = '/api/analysis/base/situation/0df0e162-8660-46dd-94d0-c6cd10324b4e/space/0'

u1 = '/moocapi/favorite/addFavoriteRecord?questionId=5b611544ecad0517a0c4d2eb&examinationId=5b67e69b267bc1138c0733a8&answerRecordId=5bea94ed267bc10a00f029fc'
u2 = '/moocapi/favorite/addFavoriteRecord?questionId=5b611c9cecad0517a0c4d316&examinationId=5b67e69b267bc1138c0733a8&answerRecordId=5bea94ed267bc10a00f029fc'
u3 = '/tvapi/question/list?questionIds=336464'
u4 = '/tvapi/question/list?questionIds=318994'


def is_same(u1, u2):
    if u1 == u3:
        return True
    f1 = u1.find('?')
    f2 = u2.find('?')
    if f1>0 and f2 >0:
        u1s = u1.split('?')
        u2s = u2.split('?')
        if u1s[0] == u2s[0]:
            return True
    flag = compare_url(u1, u2)
    if flag:
        return flag
    return False


result = is_same(uri, url)
print(result)
