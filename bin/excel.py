# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 13:39
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : excel.py
# @Software: PyCharm

import xlrd
from config.config import *
from lib.mysql import CourseMySql

def import_excel(file, db, sheet):
    book = xlrd.open_workbook(file)
    sheet_data = book.sheet_by_index(sheet)
    rows = sheet_data.get_rows()
    t = 0
    if rows:
        for item in rows:
            point = item[0].value
            subject_class = item[1].value
            id = Hua_Id_Map.get(subject_class)
            # print(subject_class)
            if id and point:
                subject = db.query_course_by_id(id)
                if subject:
                    # print(subject)
                    point_record = db.query_course_by_name_level(point, 6, id)
                    if point_record is None:
                        sort = int(subject[6])
                        data = {
                                'fid': subject[0],
                                'name': point,
                                'node_level': 6,
                                'path_info': subject[4],
                                'term': subject[5],
                                'sort': sort,
                                'name_remark': ''
                            }
                        # print(data)
                        cid = db.add_course_info(data)
                        if cid >0 :
                            t += 1
    return t

if __name__ == '__main__':
    file = DATA_PATH + '/huaxue.xlsx'
    db = CourseMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_temp_course_structure_tree'
    )
    sheet =0
    t = import_excel(file, db, sheet)
    print(t)