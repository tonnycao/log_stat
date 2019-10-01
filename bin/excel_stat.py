import xlwt
from config.config import *
from lib.mysql import VideoMySql
from lib.mysql import ChapterMySql
from lib.mysql import QuestionMySql

video_db = VideoMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_tmp_course_video_detail_bak'
)

chapter_db = ChapterMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_hsd_chapter'
)

question_db = QuestionMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                          charset=MYSQL_CHARSET, table='tb_hsd_question'
                          )

course_table = 'tb_course_structure_tree_1111'
video_table = 'tb_course_video_detail'
data = video_db.export_data(course_table, video_table)
workbook = xlwt.Workbook(encoding='utf-8')
table_name = '有题目老数据课程'
sheet = workbook.add_sheet(table_name, cell_overwrite_ok=True)
fields = ('章ID', '节ID', '章名称', '节名称', '题目统计')
for field in range(0, len(fields)):
    sheet.write(0, field, fields[field])

row = 1
for item in data:
    for index in range(0, len(fields)-1):
        sheet.write(row, index, item[index])
        stat = 0
        print(item[1])
        qids = video_db.query_question_id_by_course(item[1])
        if qids is not None and len(qids) > 0:
            result = question_db.total_stat_question_by_chapters(qids)
            if result is not None:
                stat = result
        sheet.write(row, 4, stat)
    row += 1

new_course_table = 'tb_tmp_course_structure_tree'
new_video_table = 'tb_tmp_course_video_detail_bak'
new_data = video_db.export_data(new_course_table, new_video_table)

new_sheet = workbook.add_sheet('新有题目的课程', cell_overwrite_ok=True)

fields = ('章ID', '节ID', '章名称', '节名称', '题目统计')
for field in range(0, len(fields)):
    new_sheet.write(0, field, fields[field])

row = 1
for item in new_data:
    for index in range(0, len(fields)-1):
        new_sheet.write(row, index, item[index])
    stat = 0
    qids = video_db.query_question_id_by_course(item[1])
    if qids is not None and len(qids) > 0:
        result = question_db.total_stat_question_by_chapters(qids)
        if result is not None:
            stat = result
    new_sheet.write(row, 4, stat)
    row += 1

no_question_data = video_db.no_question_data(new_course_table, new_video_table)
no_sheet = workbook.add_sheet('新无题目的课程', cell_overwrite_ok=True)
for field in range(0, len(fields)-1):
    no_sheet.write(0, field, fields[field])

row = 1
for item in no_question_data:
    for index in range(0, len(fields)-1):
        no_sheet.write(row, index, item[index])
    stat = 0
    qids = video_db.query_question_id_by_course(item[1])
    if qids is not None and len(qids) > 0:
        result = question_db.total_stat_question_by_chapters(qids)
        if result is not None:
            stat = result
    no_sheet.write(row, 4, stat)
    row += 1

# 结构题目
chapters = chapter_db.export_data()
chapter_sheet = workbook.add_sheet('华师大题目的结构', cell_overwrite_ok=True)
chapter_fields = ('篇名称', '章名称', '节名称', '年级', '题目统计')
for field in range(0, len(chapter_fields)):
    chapter_sheet.write(0, field, chapter_fields[field])

chapter_row = 1
for item in chapters:
    for index in range(0, len(chapter_fields)-1):
        chapter_sheet.write(chapter_row, index, item[index])
    stat = 0
    result = question_db.stat_question_by_chapter(item[5])
    if result is not None:
        stat = result
    chapter_sheet.write(row, 4, stat)
    chapter_row += 1

not_video_data = chapter_db.not_video_data(new_video_table)

no_video_sheet = workbook.add_sheet('新无视频华师大题目', cell_overwrite_ok=True)
chapter_fields = ('篇名称', '章名称', '节名称', '年级', '题目统计')
for field in range(0, len(chapter_fields)):
    no_video_sheet.write(0, field, chapter_fields[field])

chapter_row = 1
for item in not_video_data:
    for index in range(0, len(chapter_fields)-1):
        no_video_sheet.write(chapter_row, index, item[index])
    stat = 0
    result = question_db.stat_question_by_chapter(item[5])
    if result is not None:
        stat = result
    no_video_sheet.write(row, 4, stat)
    chapter_row += 1

workbook.save('course_video_stat.xls')



