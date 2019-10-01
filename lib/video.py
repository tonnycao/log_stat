# -*- coding:utf-8 -*-
import xlrd
from config.config import *
from lib.mysql import CourseMySql
from lib.mysql import TeacherMySql
from lib.mysql import SchoolMySql
from lib.mysql import VideoMySql
from lib.mysql import RawMySql


class Video():

    def __init__(self, course, teacher, school, video, raw):
        self.course_db = course
        self.teacher_db = teacher
        self.school_db = school
        self.video_db = video
        self.raw_db = raw

    def read(self, file, logfile, sheet_index):
        book = xlrd.open_workbook(filename=file, logfile=logfile)  # 打开一个excel
        sheet = book.sheet_by_index(sheet_index)  # 根据顺序获取sheet
        data = []
        school = set()
        teacher = set()
        s = 0
        for item in sheet.get_rows():
            if s >0 :
                i = {
                    # 文件名
                    'file': ''.join(item[0].value.split()),
                    # 视频名称
                    'name': ''.join(item[1].value.split()),
                    # 篇
                    'sheet': ''.join(item[2].value.split()),
                    # 章
                    'chapter': ''.join(item[3].value.split()) if type(item[3].value) is str else item[3].value,
                    # 节
                    'section': ''.join(item[4].value.split()) if type(item[4].value) is str else item[4].value,
                    # 知识点
                    'point': ''.join(item[5].value.split()) if type(item[5].value) is str else item[5].value,
                    # 学校
                    'school': item[6].value.split()[0] if len(item[6].value.split())>0 else item[6].value.split(),
                    # 老师
                    'teacher': item[7].value.split()[0] if len(item[7].value.split())>0 else item[7].value.split(),
                    # 年级
                    'grade': int(item[8].value) if type(item[8].value) is float else 0,
                    # 学科
                    'subject': item[9].value,
                    # 冲刺
                    'sprint': item[10].value,
                    # 获奖
                    'award': item[11].value,
                    # 名师
                    'famous': item[12].value,
                    # 精选
                    'select': item[13].value,
                    # 学期
                    'term': int(item[14].value) if type(item[14].value) is float else 0,
                    # 获奖来源
                    'award_source': item[15].value,
                    # 研究课程
                    'research': int(item[16].value) if type(item[16].value) is float else 0,
                    # 是否免费
                    'free': item[17].value,
                    # 备注
                    'remark': item[18].value
                }

                if i.get('school'):
                    school.add(i.get('school'))

                if i.get('teacher'):
                    string = i.get('teacher')
                    teacher.add(self._first(string))
                data.append(i)
            s += 1
        return data, school, teacher

    def add_video(self, item):
        raw = self.raw_db.query_data(item.get('file'))
        if raw is None:
            self.raw_db.add_data(item)
        else:
            pass

    def raw_stat(self, grade=None, subject=None, term=None):
        total = self.raw_db.stat_data(grade, subject, term)
        return total

    def raw(self, items):
        del items[0]
        for item in items:
            self.add_video(item)

    def schools(self, items):
        for item in items:
            self._add_school(item)

    def _add_school(self, item):
        school = self.school_db.query_school_by_name(item)
        id = None
        if school is None:
            school_dict = {'name': item}
            id = self.school_db.add_school(school_dict)
        return id

    def courses(self, list_dict):
        for item in list_dict:

            sheet = item.get('sheet')
            grade = item.get('grade')
            subject = item.get('subject')
            term = item.get('term')
            chapter = item.get('chapter')
            section = item.get('section')
            point = item.get('point')

            if sheet and grade and subject:
                sheet_record = self._sheet_v2(sheet, grade, subject, term)
                if sheet_record is None:
                    sheet_record = {
                        'name': sheet,
                        'grade': grade,
                        'subject': subject,
                        'term': term
                    }
                    self._add_sheet(sheet_record)
                print(sheet_record)
            #
            #     if chapter:
            #         chapter_record = self._course(chapter, sheet_record.get('id'), sheet_record.get('node_level'))
            #         print(chapter_record)
            #         if chapter_record is None:
            #             record = {
            #                 'name': chapter,
            #                 'grade': grade,
            #                 'subject': subject,
            #                 'term': term,
            #                 'fid': sheet_record.get('id'),
            #                 'node_level': int(sheet_record.get('node_level')) + 1,
            #                 'path_info': sheet_record.get('path_info')
            #             }
            #             chapter_record = self._add_course(record)
            #
                if point:
                        point_record = self._course(point, sheet_record.get('id'), sheet_record.get('node_level'))
                        if point_record is None:
                            record = {
                                'name': point,
                                'grade': grade,
                                'subject': subject,
                                'term': term,
                                'fid': sheet_record.get('id'),
                                'node_level': int(sheet_record.get('node_level')) + 1,
                                'path_info': sheet_record.get('path_info'),
                                'name_remark': section
                            }
                            point_record = self._add_course(record)


    def _course(self, name, parent_id, parent_level):
        c = None
        level = int(parent_level) + 1
        fid = int(parent_id)
        result = self.course_db.query_course_by_name_level(name, level, fid)
        if result is not None:
            c = {
                'id': result[0],
                'name': name,
                'fid': fid,
                'node_level': result[3],
                'path_info': result[4]
            }
        return c

    def _add_sheet(self, sheet_dict):
        subject_name = GradeMap[str(sheet_dict.get('grade'))] + sheet_dict.get('subject')
        subject = self.course_db.query_course_by_name(subject_name)

        fid = subject[0]
        level = subject[3]
        path_info = subject[4]
        item = {
            'name': sheet_dict.get('name'),
            'term': sheet_dict.get('term'),
            'sort': SortMap[str(sheet_dict.get('grade'))] if sheet_dict.get('grade')>0 else 100,
            'fid': fid,
            'node_level': int(level)+1,
            'path_info': path_info,
            'name_remark': '',
            'status': 1
        }
        id = self.course_db.add_course_detail(item)
        if id >0:
            sheet_dict['id'] = id
            sheet_dict['fid'] = fid
            sheet_dict['node_level'] = item.get('node_level')
            sheet_dict['path_info'] = item.get('path_info')+','+str(id)
            self.course_db.update_course_path_by_id(id, sheet_dict['path_info'])
        return id

    def grade(self, items):
        for item in items:
            __grade = item.get('grade')
            if __grade:
                grade_record = self._grade(__grade)
                if grade_record is None:
                    self._add_grade(__grade)

    def course_stat(self, level):
        stat = self.course_db.stat_by_level(level)
        return stat

    # 获取年级信息
    def _grade(self, grade):
        name = GradeMap[str(grade)]
        data = self.course_db.query_course_by_name(name)
        return data

    # 保存年级信息
    def _add_grade(self, grade):
        name = GradeMap.get(str(grade))
        fid = self._get_fid(grade)
        level = self._get_level(grade)
        sort = self._get_sort(grade)
        data = {
            'name': name,
            'fid': fid,
            'path_info': '',
            'node_level': level,
            'term': 0,
            'name_remark': '',
            'sort': sort,
            'status': 0
        }
        return self.course_db.add_course_detail(data)

    # 处理科目并返回ID
    def _subject(self, name, grade, term):
        _grade = GradeMap.get(str(grade))
        id = 0
        if _grade:
            name =  _grade + name
            data = self.course_db.query_course_by_name(name, term)
            if data is None:
                level = self._get_level(grade)+1
                fid = self._get_fid(grade)
                sort = self._get_sort(grade)
                data = {
                    'name': name,
                    'fid': fid,
                    'path_info': '',
                    'node_level': level,
                    'term': term,
                    'name_remark': '',
                    'sort': sort,
                    'status': 0
                }
                id = self.course_db.add_course_detail(data)
            else:
                id = data[0]
        return id

    # 批量处理科目
    def subject(self, items):
        for item in items:
            self._subject(item['subject'], item['grade'], item['term'])

    # 年级的级别
    def _get_level(self, grade):
        level = GradeLevelMap.get(str(grade))
        return level

    # 年级的FID
    def _get_fid(self, grade):
        fid = GradeFidMap.get(str(grade))
        return fid

    # 年级排序
    def _get_sort(self, grade):
        sort = SortMap.get(str(grade))
        return sort

    # 篇的信息
    def _sheet_v2(self, name, grade, subject, term):
        sheet = None
        title = GradeMap[str(grade)] + subject
        parent = self.course_db.query_course_by_name(title, term)
        if parent is None:
            return sheet
        level = int(parent[3]) + 1
        fid = parent[0]
        result = self.course_db.query_course_by_name_level(name, level, fid)
        if result is not None:
            sheet = {
                'id': result[0],
                'name': result[1],
                'fid': result[2],
                'node_level': result[3],
                'path_info': result[4],
                'term': result[5]
            }
        return sheet

    def _sheet(self, name, grade, subject):
        sheet = None
        title = GradeMap[str(grade)] + subject
        parent = self.course_db.query_course_by_name(title)
        if parent is None:
            return sheet
        level = int(parent[3]) + 1
        fid = parent[0]
        result = self.course_db.query_course_by_name_level(name, level, fid)
        if result is not None:
            sheet = {
                'id': result[0],
                'name': result[1],
                'fid': result[2],
                'node_level': result[3],
                'path_info': result[4]
            }
        return sheet

    def teachers(self, items):
        for item in items:
            self._add_teacher(item)

    # 导入视频
    def videos(self, items):
        for item in items:
            award_resource = self._award(item)
            reasearch = self._reasearch(item)
            school = self._get_school(item)
            teacher = self._get_teacher(item)
            chapter = self._get_chapter(item)
            property = self._get_property(item)
            course_structure = self._get_course_structure(item)
            vdict = {
                'foreign_course_structure_tree': course_structure,
                'foreign_course_property': property,
                'bestbox3_origin_name': item.get('file'),
                'show_name': item.get('name'),
                'foreign_question_chapter': chapter,
                'foreign_school': school,
                'foreign_teacher': teacher,
                'award_resource': award_resource,
                'foreign_reasearch_based': reasearch,
            }
            # print(vdict)
            id = self.video_db.insert_video(vdict)

    def _get_school(self, item):
        id = 0
        raw = item.get('school')
        select = item.get('select')
        if select and raw:
            name = self._first(raw)
            school = self.school_db.query_school_by_name(name)
            if school is not None:
                id = school[0]
        return id

    def _get_teacher(self, item):
        id = 0
        if item.get('famous'):
            raw = item.get('teacher')
            if raw:
                name = self._first(raw)
                teacher = self.teacher_db.query_teacher_by_name(name)
                if teacher is not None:
                    id = teacher[0]
        return id

    def _get_course_structure(self, item):
        id = 0
        sheet = item.get('sheet')
        point = item.get('point')
        grade = item.get('grade')
        subject = item.get('subject')

        if point:
            name = GradeMap[str(grade)] + subject
            grade_record = self.course_db.query_course_by_name(name)
            ffid = None
            fid = None
            if grade_record is not None:
                ffid = grade_record[0]
            if sheet:
                sheet_record = self.course_db.query_course_by_name_level(sheet, 6, ffid)
                if sheet_record is not None:
                    fid = sheet_record[0]
            point_record = self.course_db.query_course_by_name_level(point, 7, fid)
            if point_record is not None:
                id = point_record[0]
        elif sheet:
            name = GradeMap[str(grade)] + subject
            grade_record = self.course_db.query_course_by_name(name)
            ffid = None
            fid = None
            if grade_record is not None:
                ffid = grade_record[0]
            sheet_record = self.course_db.query_course_by_name_level(sheet, 6, ffid)
            if sheet_record is not None:
                id = sheet_record[0]
        return id

    # 默认是1收费课程
    def _get_property(self, item):
        property_map = {
            'fee': '1',
            'famous': '2',
            'school': '3',
            'award': '4',
            'research': '5',
            'free': '6',
            'zhongkao': '7',
            'gaokao': '8',
        }
        property = set()
        if item.get('award'):
            property.add(property_map['award'])
        if item.get('famous'):
            property.add(property_map['famous'])
        if item.get('research'):
            property.add(property_map['research'])
        if item.get('free') == '是':
            property.add(property_map['free'])
        else:
            property.add(property_map['fee'])

        if item.get('sprint') == '高考':
            property.add(property_map['gaokao'])
        elif item.get('sprint') == '中考':
            property.add(property_map['zhongkao'])

        return ','.join(property)

    def _reasearch(self, item):
        reasearch_int = 0
        # if len(item.get('research'))>0:
        #     name = item.get('name')
        #     research = self.research_db.query_by_name(name.strip())
        #     if research is not None:
        #         reasearch_int = research[0]
        #     else:
        #         reasearch_int = self.research_db.insert_data(name.strip())
        return reasearch_int

    def _award(self, item):
        award_int = 0
        map1 = {
            '一等奖': 3,
            '二等奖': 4,
            '三等奖': 5
        }
        map2 = {
            '一等奖': 6,
            '二等奖': 7,
            '三等奖': 8
        }
        award = item.get('award')
        award_reource = item.get('award_source')
        if award:
            if award_reource ==1:
                award_int = map1.get(award.strip())
            elif award_reource ==2:
                award_int = map2.get(award.strip())
        return award_int

    def _add_teacher(self, item):
        teacher = self.teacher_db.query_teacher_by_name(item)
        id = None
        if teacher is None:
            t_dict = {'name': item}
            id = self.teacher_db.add_teacher(t_dict)
        return id

    def _add_course(self, data):
        result = {
            'name': data.get('name'),
            'fid': data.get('fid'),
            'node_level': data.get('node_level'),
            'path_info': data.get('path_info'),
            'term': data.get('term'),
            'name_remark': '',
            'sort': SortMap.get(str(data.get('grade'))),
            'status': 1
        }
        remark = data.get('name_remark')
        if remark:
            result['name_remark'] = remark

        id = self.course_db.add_course_detail(result)
        if id >0:
            data['id'] = id
            data['path_info'] = data['path_info'] + ',' + str(id)
            self.course_db.update_course_path_by_id(id, data['path_info'])
        return data

    def _first(self, string):
        result = string
        if string.find("/", 0)>0:
            lists = string.split("/")
            result = lists[0]
        elif string.find("、", 0)>0:
            lists = string.split("、")
            result = lists[0]
        elif string.find("等", 0)>0:
            lists = string.split("等")
            result = lists[0]
        elif string.find(",", 0)>0:
            lists = string.split(",")
            result = lists[0]
        elif string.find("，", 0)>0:
            lists = string.split("，")
            result = lists[0]
        elif string.find("&", 0)>0:
            lists = string.split("&")
            result = lists[0]
        elif string.find(" ", 0)>0:
            lists = string.split(" ")
            result = lists[0]
        elif string.find("（", 0)>0:
            lists = string.split("（")
            result = lists[0]
        return result

if __name__ == '__main__':
    couse = CourseMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                     charset=MYSQL_CHARSET, table='tb_course_structure_tree_internet')
    teacher = TeacherMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                     charset=MYSQL_CHARSET, table='tb_tmp_teacher')
    school = SchoolMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_tmp_school')
    video = VideoMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_tmp_course_video_detail')
    raw = RawMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_tmp_course_video_raw'
    )
    videos = Video(couse, teacher, school, video, raw)
    file = DATA_PATH + '/20190718.xlsx'
    logfile = LOG_PATH + '/excel.log'
    raw_data, schools, teachers = videos.read(file, logfile, 0)
    videos.courses(raw_data)
    # videos.subject(raw_data)
    # ss = videos.course_stat(4)
    # videos.schools(schools)
    # videos.teachers(teachers)
    # print(ss)
    # tt = videos.raw_stat(grade=11, subject='化学', term=2)
    # print(tt)

    # videos.courses(raw_data)



