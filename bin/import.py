# -*- coding: utf-8 -*-
# @Time    : 2019/7/30 10:27
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : import.py
# @Software: PyCharm

from config.config import *
from lib.mysql import VideoMySql

video_local_db = VideoMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_course_video_detail'
)

video_62_db = VideoMySql(host='192.168.8.62', user='bestbox3', passwd='secret2017', port=3308, db='db_bestbox3_internet',
                    charset=MYSQL_CHARSET, table='tb_course_video_detail'
)

local_list = video_local_db.query_data_by_course(-3)
s = 0
for local in local_list:
    # print(local)
    local_total = video_62_db.query_video_by_bestbox_origin_name(local[1])
    if local_total is None:
        id = video_62_db.insert_video_by_full(local)
        if id >0:
            s += 1

print(s)