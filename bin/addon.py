# -*- coding: utf-8 -*-
# @Time    : 2019/7/30 14:40
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : addon.py
# @Software: 百视宝新增知识点数据处理程序

import xlrd
from config.config import *
from lib.mysql import CourseMySql

def key_point_handle(file, sheet, level, course_id):
    db = CourseMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_course_structure_tree'
    )

    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(sheet)
    rows = sheet.get_rows()
    total = 0
    success = 0
    i = 0

    if rows:
        for row in rows:
            if i > 0:
                if row[0].value and row[1].value and row[2].value:
                    total += 1
                    chapter = db.query_course_by_name_level(row[0].value, level+1, course_id)
                    if chapter:
                        point = db.query_course_by_name_level(row[2].value, level+2, chapter[0])
                        if point is None:
                            data = {
                                'name': row[2].value,
                                'fid': chapter[0],
                                'term': chapter[5],
                                'node_level': level+2,
                                'path_info': '',
                                'name_remark': row[1].value,
                                'status': 1,
                                'sort': 800
                            }
                            id = db.add_course_detail(data)
                            if id:
                                path = chapter[4] + ',' + str(id)
                                db.update_course_path_by_id(id, path)
                                success += 1
                    else:
                        course = db.query_course_by_id(course_id)
                        if course:
                            data = {
                                'name': row[0].value,
                                'fid': course_id,
                                'term': course[5],
                                'node_level': level + 1,
                                'path_info': '',
                                'name_remark': '',
                                'status': 1,
                                'sort': 800
                            }
                        id = db.add_course_detail(data)
                        if id :
                            path = course[4] + ',' + str(id)
                            db.update_course_path_by_id(id, path)
                            section = {
                                'name': row[2].value,
                                'fid': id,
                                'term': course[5],
                                'node_level': level + 2,
                                'path_info': '',
                                'name_remark': row[1].value,
                                'status': 1,
                                'sort': 800
                            }
                            id = db.add_course_detail(section)
                            if id:
                                path = chapter[4] + str(id)
                                db.update_course_path_by_id(id, path)
                                success += 1
            i += 1
    return (total, success)

if __name__ == '__main__':
    file = DATA_PATH + '/sample.xlsx'
    sheet = 0
    id = 96
    level = 5
    log_tuple = key_point_handle(file, sheet, level, id)
    print(log_tuple)
