# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 11:00
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : video_stat.py
# @Software: PyCharm

import xlwt
from config.config import *
from lib.mysql import VideoMySql
from lib.mysql import ChapterMySql
from lib.mysql import QuestionMySql
from lib.mysql import CourseMySql


def main():
    course_table = 'tb_course_structure_tree'
    video_table = 'tb_course_video_detail'
    chapter_table = 'tb_hsd_chapter'
    question_table = 'tb_hsd_question'

    video_db = VideoMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                          charset=MYSQL_CHARSET, table=video_table
                          )

    chapter_db = ChapterMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                              charset=MYSQL_CHARSET, table=chapter_table
                              )

    question_db = QuestionMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                                charset=MYSQL_CHARSET, table=question_table
                                )

    course_db = CourseMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                            charset=MYSQL_CHARSET, table=course_table
                            )

    fields = ('章ID', '节ID', '年级课程', '章名称', '节名称', '视频统计')
    excel = xlwt.Workbook(encoding='utf-8')
    term_dict = {
        '0': '',
        '1': '上学期',
        '2': '下学期',
        '3': '拓展上',
        '4': '拓展下'
    }

    sheet_name = '课程视频统计'
    sheet = excel.add_sheet(sheet_name, cell_overwrite_ok=True)
    # init first row
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field])

    data = course_db.query_course_by_node_level(str(5))
    j = 1
    for item in data:
        name = item[1]
        path_info = item[2]
        term = term_dict.get(str(item[3]))
        class_name = name+term
        data = course_db.query_course_structure_by_path(path_info=path_info)

        for i in data:
            stat = video_db.stat_video_data(str(i[1]))
            course = course_db.query_course_by_id(i[1])
            if stat == 0 and course[7]==1:
                course_db.update_status_by_id(i[1], 0)
                sheet.write(j, 0, i[0])
                sheet.write(j, 1, i[1])
                sheet.write(j, 2, class_name)
                sheet.write(j, 3, i[3])
                sheet.write(j, 4, i[4])
                sheet.write(j, 5, stat)
                j += 1

    excel.save(DATA_PATH + '/course_no_video.xls')


if __name__ == '__main__':
    main()


