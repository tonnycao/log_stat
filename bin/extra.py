# -*- coding: utf-8 -*-
# @Time    : 2019/7/29 13:42
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : extra.py
# @Software: PyCharm
from config.config import *
import xlrd
import logging
import logging.config
from lib.mysql import VideoMySql

if __name__ == '__main__':
    file = DATA_PATH + '/list.xls'
    log_file = LOG_PATH + '/log.log'
    logger = logging.getLogger('log')
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(filename=log_file, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    video_db = VideoMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_course_video_detail'
    )
    sheet_index = 2
    book = xlrd.open_workbook(file, logfile=logger)
    sheet = book.sheet_by_index(sheet_index)
    sheet_name = sheet.name

    rows = sheet.get_rows()
    total = 0
    success = 0
    if rows:
        for i in rows:
            total += 1
            if i[0].value and i[1].value:
                bestbox3_origin_name = i[0].value
                origin_name = i[1].value
                video = video_db.query_video_by_name(bestbox3_origin_name)
                if video is None:
                    data = {
                        'foreign_course_structure_tree': 0,
                        'foreign_course_property': 0,
                        'bestbox3_origin_name': bestbox3_origin_name,
                        'origin_name': origin_name,
                        'show_name': sheet_name
                    }
                    logger.info(bestbox3_origin_name[0] + ":" + origin_name)
                    video_db.insert_video_by_short(data)
                    success += 1
                elif video[4] != origin_name:
                    video_db.update_by_origin_name(video[0], origin_name)
                    logger.warning(video[0] + ":" + origin_name)
                    success += 1
    print(success)
    print(total)
