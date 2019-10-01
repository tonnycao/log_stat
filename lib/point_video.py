# -*- coding:utf-8 -*-
import xlrd
from config.config import *
from lib.mysql import CourseMySql
from lib.mysql import TeacherMySql
from lib.mysql import SchoolMySql
from lib.mysql import VideoMySql
from lib.mysql import RawMySql


class PointVideo():

    def __init__(self, course, video, raw, teacher, school):
        self.course_db = course
        self.video_db = video
        self.raw_db = raw
        self.teacher_db = teacher
        self.school_db = school

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
                    # 知识点
                    'point': ''.join(item[2].value.split()) if type(item[2].value) is str else item[2].value,
                    'sheet': '',
                    'chapter': '',
                    'section': '',
                    # 年级
                    'grade_str':  item[3].value,
                    # 学校
                    'school': item[4].value,
                    # 老师
                    'teacher': item[5].value,
                    # 年级
                    'grade': int(item[6].value) if type(item[6].value) is float else 0,
                    # 学科
                    'subject': item[7].value,
                    # 冲刺
                    'sprint': item[8].value,
                    # 获奖
                    'award': item[9].value,
                    # 名师
                    'famous': item[10].value,
                    # 精选
                    'select': item[11].value,
                    # 学期
                    'term': int(item[12].value) if type(item[12].value) is float else 0,
                    # 获奖来源
                    'award_source': item[13].value,
                    # 研究课程
                    'research': int(item[14].value) if type(item[14].value) is float else 0,
                    # 是否免费
                    'free': item[15].value,
                    'remark': ''
                }
                data.append(i)
            s += 1
        return data

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

    # 知识点
    def courses_points(self, list_dict):
        s = 0
        for item in list_dict:
            subject = item.get('subject')
            grade = item.get('grade')
            term = item.get('term')
            point = item.get('point')
            if grade > 0 and point and subject:
                title = GradeMap[str(grade)] + subject
                subject_record = self.course_db.query_course_by_name(title, term)
                if subject_record:
                    point_record = self._course(point, subject_record[0], subject_record[3])
                    if point_record is None:
                        record = {
                            'name': point,
                            'grade': grade,
                            'subject': subject,
                            'term': term,
                            'fid': subject_record[0],
                            'node_level': int(subject_record[3]) + 1,
                            'path_info': subject_record[4],
                            'name_remark': ''
                        }
                        point_record = self._add_course(record)
                        if point_record['id']:
                            s += 1
        return s

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
        state = 0

        for item in items:
            award_resource = self._award(item)
            reasearch = self._reasearch(item)
            school = self._get_school(item)
            teacher = self._get_teacher(item)
            chapter = ''
            property = self._get_property(item)
            # print(item)
            course_structure = self._get_course_structure(item)
            # print(course_structure)
            video_record = self.video_db.query_video_by_bestbox_origin_name(item.get('file'))
            if video_record is None:
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
                id = self.video_db.insert_video(vdict)
                if id >0:
                    state += 1
            else:
                result = self.video_db.update_foreign(video_record[0], course_structure)
                if result:
                    state += 1
        return state

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
        term = item.get('term') if item.get('term')>0 else 0
        if point:
            name = GradeMap[str(grade)] + subject
            grade_record = self.course_db.query_course_by_name(name, term)
            ffid = None
            fid = None
            if grade_record is not None:
                ffid = grade_record[0]
                id = grade_record[0]
                fid = grade_record[0]
            if sheet:
                sheet_record = self.course_db.query_course_by_name_fid(sheet, ffid)
                if sheet_record is not None:
                    fid = sheet_record[0]
                    id = sheet_record
            point_record = self.course_db.query_course_by_name_fid(point, fid)
            if point_record is not None:
                id = point_record[0]
        elif sheet:
            name = GradeMap[str(grade)] + subject
            grade_record = self.course_db.query_course_by_name(name)
            fid = None
            if grade_record is not None:
                fid = grade_record[0]
                id = grade_record[0]
            sheet_record = self.course_db.query_course_by_name_fid(sheet, fid)
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
                     charset=MYSQL_CHARSET, table='tb_temp_course_structure_tree')

    video = VideoMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_temp_course_video_detail')

    teacher = TeacherMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                          charset=MYSQL_CHARSET, table='tb_teacher'
                          )
    school = SchoolMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                         charset=MYSQL_CHARSET, table='tb_school'
                         )

    raw = RawMySql(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
        charset=MYSQL_CHARSET, table='tb_temp_course_video_raw'
    )

    videos = PointVideo(couse, video, raw, teacher, school)
    file = DATA_PATH + '/20190802.xlsx'
    logfile = LOG_PATH + '/excel.log'
    raw_data = videos.read(file, logfile, 0)
    stat = videos.videos(raw_data)
    print(stat)
    # stat = videos.courses_points(raw_data)
    # print(stat)



