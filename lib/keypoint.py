# -*- coding:utf-8 -*-
import xlrd
from config.config import *
from lib.mysql import CourseMySql

'''
@author Tonny Cao
@todo 只包含知识点的excel导入
@date 2019-07-15
'''


class Keypoint:
    def __init__(self, db, debug_flag, level):
        self.db = db
        self.debug = debug_flag
        self.level = level

    def read(self, file, sheet_index):
        book = xlrd.open_workbook(file)  # 打开一个excel
        sheet = book.sheet_by_index(sheet_index)  # 根据顺序获取sheet
        rows = []
        stat = 0
        ncols = sheet.ncols
        if ncols > 0 :
            print(ncols)
        for item in sheet.get_rows():
            if self.debug:
                string = ''
                for i in range(ncols):
                    string += str(item[i].value) + ' '
                print(string)

            if stat > 0 and len(item)>0:
                kdict = self._format_dict(item, sheet_index)
                if self.debug:
                    print(kdict)
                rows.append(kdict)
            stat += 1
        return rows

    # 批量入库
    def insert_keypoint(self, rows):
        for row in rows:
            self.insert_item(row)

    # 入库
    def insert_item(self, item):
        name = item.get('value')
        fid = 0
        path_info = ''
        parent = self.db.query_course_by_name(item.get('title'))
        if parent is not None:
            if self.debug:
                print(parent)
            path_info = parent[-1] + ',' + str(parent[0])
            fid = parent[0]

        course = {
            'fid': fid,
            'name': name,
            'level': int(self.level),
            'path_info': path_info,
            'sort': 0,
            'term': int(item.get('term')),
            'status': 1
        }

        if self.debug:
            print(course)
        else:
            id = self.db.add_course_detail(course)
            if id is not None:
                self.db.update_course_sort_by_id(id)

    def _format_dict(self, row, index):
        if index == 0 :
            default_course = '语文'
        elif index == 1:
            default_course = '英语'
        elif index == 2:
            default_course = '数学'
        elif index == 3:
            default_course = '物理'
        else:
            default_course = '化学'

        if index == 0 or index == 1:
            grade = int(row[3].value)
            title = GradeMap.get(str(grade))
            kdict = {
                    'course': default_course,
                    'grade': grade,
                    'value': row[4].value,
                    'title': title + default_course,
                    'term': 0
                }
        else:
            grade = int(row[1].value)
            title = GradeMap.get(str(grade))
            kdict = {
                'course': default_course,
                'grade': int(row[1].value),
                'value': row[0].value,
                'title': title+default_course,
                'term': int(row[3].value) if row[3].value else 0
            }
        return kdict

if __name__ == '__main__':
    db = CourseMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                     charset=MYSQL_CHARSET, table=MYSQL_TABLE)
    key = Keypoint(db, True, KeyPoint_Level)
    file = '20190712.xlsx'
    # chinese_key_point = key.read(file, 0)
    # key.insert_keypoint(chinese_key_point)

    # math_key_point = key.read(file, 2)
    # key.insert_keypoint(math_key_point)
    # english_key_point = key.read(file, 1)
    # key.insert_keypoint(english_key_point)
    # wuli_key_point = key.read(file, 3)
    # key.insert_keypoint(wuli_key_point)
    huaxue_key_point = key.read(file, 4)
    # key.insert_keypoint(huaxue_key_point)