from config.config import *
from lib.mysql import CourseMySql

course_db = CourseMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                        charset=MYSQL_CHARSET, table='tb_course_structure_tree'
                        )
grade_courses = course_db.query_course_by_level(5)
chapter_courses = course_db.query_course_by_level(6)

for chapter in chapter_courses:
    # print(chapter)
    id = chapter[0]
    fid = chapter[2]
    term = chapter[4]
    new_fid = 0
    name = ''
    for grade in grade_courses:
        if fid == grade[0] and term != grade[4]:
            name = grade[1]
    if len(name) > 0:
        for grade in grade_courses:
            if name == grade[1] and term == grade[4]:
                new_fid = grade[0]
    if new_fid > 0 and len(name) > 0:
        course_db.update_course_fid(id, new_fid)