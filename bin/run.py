# -*- coding:utf-8 -*-

from lib.mysql import CourseMySql
from lib.course import Course
from config.config import *


def main():
    cm = CourseMySql(host =MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                      charset=MYSQL_CHARSET, table=MYSQL_TABLE)

    c = Course(cm, DEBUG_MODEL, 'huaxue.xlsx', Course_HuaXue_Map, Chapter_Level, KeyPoint_Level)
    courses = c.get_course_path(798)
    print(courses)
    cm.close()


if __name__ == '__main__':
    main()
