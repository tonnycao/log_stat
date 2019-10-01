# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 9:40
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : txt.py
# @Software: PyCharm
import uuid
from config.config import *
name = 'test_name'
# namespace = 'test_namespace'
namespace = uuid.NAMESPACE_URL

print(uuid.uuid1())
print(uuid.uuid3(namespace,name))
print(uuid.uuid4())
print(uuid.uuid5(namespace,name))
print(len('62740382-6394-5d1c-b9ef-d5a953ac1213'))
file = DATA_PATH + '/query.txt'
with open(file, 'r', encoding='utf-8') as c:
    print(c.readline())


