# -*- coding:utf-8 -*-

import xlrd
'''
包含章节的excel导入
'''

class Course():
    db = None
    debug = True
    file = None
    course_map = None
    chapter_level = None
    keypoint_level = None

    def __init__(self, db, debug_flag, file, course_map, chapter_level, keypoint_level):
        self.file = file
        self.course_map = course_map
        self.chapter_level = chapter_level
        self.keypoint_level = keypoint_level
        self.db = db
        self.debug = debug_flag

    def read_excel(self, sheet_index):
        book = xlrd.open_workbook(self.file)  # 打开一个excel
        sheet = book.sheet_by_index(sheet_index)  # 根据顺序获取sheet
        rows = []
        stat = 0
        for i in sheet.get_rows():
            if self.debug is True:
                print(str(i[0].value) + ',' + i[1].value + ',' + i[2].value)
            if stat > 0:
                subject = self.course_map.get(str(i[0].value))
                course = {
                    'subject': subject,
                    'chapter': i[1].value,
                    'keypoint': i[2].value,
                }
                rows.append(course)
            stat += 1
        return rows

    def get_subject(self, name):
        level = int(self.chapter_level)-1
        subject = self.db.query_course_by_name_level(name, level)
        return subject

    def get_chapter(self, name, level):
        chapter = self.db.query_course_by_name_level(name, level)
        if chapter is not None:
            return chapter
        else:
            return None

    def get_course(self, id):
        course = self.db.query_course_by_id(id)
        if course is not None:
            return course
        else:
            return None

    def get_course_path(self, id):
        paths = []
        path = ''
        course = self.get_course(id)
        if course is not None and course[2] > 0:
            parent_course = self.get_course(course[2])
            if parent_course is not None and parent_course[4] is not None and len(parent_course[4]) > 0:
                path = path + parent_course[4] + ',' + parent_course[0]
            elif parent_course is not None and parent_course[2] > 0:
                paths.append(parent_course[0])
                last_course = self.get_course(parent_course[2])
                if last_course is not None and last_course[4] is not None and len(last_course[4]) > 0:
                    paths_str = ','.join(str(s) for s in paths if s not in [None, 0])
                    path = path + last_course[4] + ',' + paths_str
                elif last_course is not None:
                    paths.append(last_course[0])
                    if last_course[2] > 0:
                        next_course = self.get_course(last_course[2])
                        if next_course is not None and next_course[4] is not None and len(next_course[4]) > 0:
                            paths_str = ','.join(str(s) for s in paths if s not in [None, 0])
                            path = path + next_course[4] + ',' + paths_str
        return path

    def format_chapter(self, row, fid):
        data = None
        if row['chapter'] is not None and len(row['chapter']) > 0:
            data = {
                    'name': row['chapter'],
                    'level': self.chapter_level,
                    'fid': fid
            }
        return data

    def format_keypoint(self, row, fid):
        data = None
        if row['keypoint'] is not None and len(row['keypoint']) > 0:
            data = {
                    'fid': fid,
                    'name': row['keypoint'],
                    'level': self.keypoint_level
            }
        return data

    def add_data(self, row, subject_id):
        chapter = self.format_chapter(row, subject_id)
        if chapter is not None:
            stat = self.db.stat_course_by_name_level(chapter['name'], chapter['level'], chapter['fid'])
            if self.debug is True:
                stat = 1
                print(chapter)
                keypoint = self.format_keypoint(row, 1)
                print(keypoint)

            if stat == 0 :
                fid = self.db.add_course(chapter)
                if fid is not None:
                    keypoint = self.format_keypoint(row, fid)
                    if keypoint is not None:
                        keypoint_stat = self.db.stat_course_by_name_level(keypoint['name'], keypoint['level'], keypoint['fid'])
                        if self.debug is True:
                            keypoint_stat = 1
                            print(keypoint)

                        if keypoint_stat == 0 :
                            self.db.add_course(keypoint)
        else:
            chapter_record = self.db.query_course_by_name_level(chapter['name'], chapter['level'], chapter['fid'])
            if self.debug is True:
                print(chapter_record)
            if chapter_record is not None:
                keypoint = self.format_keypoint(row, chapter_record[0])
                if keypoint is not None:
                    keypoint_stat = self.db.stat_course_by_name_level(keypoint['name'], keypoint['level'], keypoint['fid'])
                    if self.debug is True:
                        keypoint_stat = 1
                        print(keypoint)
                    if keypoint_stat == 0 :
                        self.db.add_course(keypoint)