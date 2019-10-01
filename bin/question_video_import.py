# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 9:34
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : question_video_import.py
# @Software: PyCharm
import time
import xlrd
from config.config import *
from lib.mysql import VideoMySql


def import_excel(file, sheet):
    data = []
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(sheet)
    rows = sheet.get_rows()
    for row in rows:
        item = {
         'bestbox3_origin_name': row[0].value,
         'origin_name': row[1].value,
        }
        data.append(item)

    return data


def insert_db(db, data):
    state = 0
    for i in data:
        item = {
            'foreign_course_structure_tree': 0,
            'foreign_course_property': 0,
            'bestbox3_origin_name': i['bestbox3_origin_name'],
            'origin_name': i['origin_name'],
            'show_name': '20190929增加清单（877个）'
        }
        id_no = db.insert_video_by_short(item)
        if id_no >0:
            state += 1

    return state

if __name__ == '__main__':
    start_time = time.time()
    file = DATA_PATH + '/20190929.xlsx'
    sheet = 0
    row_data = import_excel(file, sheet)
    video_db = VideoMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_course_video_detail')
    total = insert_db(video_db,row_data)
    end_time = time.time()
    span_time = end_time - start_time
    print('total import: ' + str(total))
    print('span time:' + str(span_time))