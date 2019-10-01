import pymysql
from config.config import *


# mysql 基类
class MySql:
    logfile = LOG_PATH + '/mysql.log'

    def __init__(self, host, user, passwd, port, db, charset, table):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
        self.charset = charset
        self.table = table
        self._connect()

    def _connect(self):
        self.connect = pymysql.connect(host=self.host, user=self.user, password=self.passwd, port=self.port, db=self.db,
                                       charset=self.charset)
        self.cursor = self.connect.cursor()

    def execute_sql_with_one_data(self, sql):
        row = None
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
        except Exception as e:
            file = open(self.logfile, 'a+', encoding='utf8')
            file.write(sql + '\n')
            file.write(str(e) + '\n')
            self.connect.rollback()
        return row

    def execute_sql_with_many_data(self, sql, size=100):
        rows = None
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchmany(size)
        except Exception as e:
            file = open(self.logfile, 'a+', encoding='utf8')
            file.write(sql + '\n')
            file.write(str(e) + '\n')
            self.connect.rollback()
        return rows

    def execute_sql_with_id(self, sql):
        last_id = 0
        try:
            if self.cursor.execute(sql):
                self.connect.commit()
                last_id = self.cursor.lastrowid
        except Exception as e:
            file = open(self.logfile, mode='a+', encoding='utf8')
            file.write(sql+'\n')
            file.write(str(e) + '\n')
            self.connect.rollback()
        return last_id

    def execute_sql_without_data(self, sql):
        try:
            if self.cursor.execute(sql):
                self.connect.commit()
        except Exception as e:
            file = open(self.logfile, 'a+', encoding='utf8')
            file.write(sql + '\n')
            file.write(str(e) + '\n')
            self.connect.rollback()

    def close(self):
        self.cursor.close()
        self.connect.close()


# 原始数据
class RawMySql(MySql):
    def __init__(self, host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def query_data(self, file):
        sql = "SELECT `file`,`file_name`,`sheet`,`chapter`,`section`,`point`,`grade`,`subject`,`term` FROM " + self.table + " WHERE file='{0}'".format(file)
        data = self.execute_sql_with_one_data(sql)
        return data

    def add_data(self, raw_dict):
        sql = "INSERT INTO " + self.table + \
              "(`file`,`file_name`,`sheet`,`chapter`,`section`,`point`,`school`,`teacher`," \
              "`grade`,`subject`,`sprint`,`award`,`award_source`,`famous`,`choose`," \
              "`term`,`research`,`free`,`remark`) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}'," \
              "'{6}','{7}',{8},'{9}','{10}','{11}','{12}','{13}','{14}',{15},'{16}','{17}','{18}')".format(
                  raw_dict['file'], pymysql.escape_string(raw_dict['name']), raw_dict['sheet'],
                  raw_dict['chapter'], raw_dict['section'], raw_dict['point'],
                  raw_dict['school'], raw_dict['teacher'], raw_dict['grade'], raw_dict['subject'], raw_dict['sprint'], raw_dict['award'],
                  raw_dict['award_source'], raw_dict['famous'], raw_dict['select'], raw_dict['term'],
                  raw_dict['research'], raw_dict['free'], raw_dict['remark']
              )
        return self.execute_sql_with_id(sql)

    def delete_data(self, grade=None, subject=None, term=None):
        where = " 1"
        if grade:
            where += " AND grade=" + int(grade)
        if subject:
            where += " AND subject='" + pymysql.escape_string(subject) + "'"
        if term:
            where += " AND term=" + int(term)
        sql = "DELETE FROM " + self.table + " WHERE " + where
        self.execute_sql_without_data(sql)

    def truncate_data(self):
        sql = "TRUNCATE TABLE "+ self.table
        self.execute_sql_without_data(sql)

    def stat_data(self, grade=None, subject=None, term=None):
        total = 0
        where = " 1"
        if grade:
            where += " AND grade=" + str(grade)
        if subject:
            where += " AND subject='" + pymysql.escape_string(subject) + "'"
        if term:
            where += " AND term=" + str(term)
        sql = "SELECT count(*) AS total FROM " + self.table + " WHERE " + where
        data = self.execute_sql_with_one_data(sql)
        if data:
            total = data[0]
        return total


# 课程
class CourseMySql(MySql):

    def __init__(self,  host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def add_course(self, course_dict):
        sql = "INSERT INTO "+self.table+"(fid,name,node_level) VALUES({0}, '{1}', {2})".format(course_dict['fid'], pymysql.escape_string(course_dict['name']),course_dict['level'])
        id = self.execute_sql_with_id(sql)
        return id

    def add_course_info(self, course_dict):
        sql = "INSERT INTO " + self.table + \
              "(fid,name,node_level,path_info,term,sort,name_remark) VALUES({0},'{1}',{2},'{3}',{4},{5},'{6}')".\
                  format(course_dict['fid'], pymysql.escape_string(course_dict['name']), course_dict['node_level'], course_dict['path_info'],
                         course_dict['term'], course_dict['sort'], course_dict['name_remark'])
        id = self.execute_sql_with_id(sql)
        return id

    def add_course_detail(self, course_dict):
        sql = "INSERT INTO " + self.table + \
              "(fid,name,node_level,path_info,term,sort,status,name_remark)" \
              " VALUES({0},'{1}',{2},'{3}',{4},{5},{6},'{7}')".\
                  format(course_dict['fid'], pymysql.escape_string(course_dict['name']), course_dict['node_level'], course_dict['path_info'],
                         course_dict['term'], course_dict['sort'], course_dict['status'], pymysql.escape_string(course_dict['name_remark']) )

        id = self.execute_sql_with_id(sql)
        return id

    def query_course_by_id(self, id):
        sql = "SELECT id,name,fid,node_level,path_info,term,sort,status FROM "+self.table+" WHERE id={0}".format(id)
        course = self.execute_sql_with_one_data(sql)
        return course

    def query_course_by_name(self, name, term=None):
        if term is not None:
            sql = "SELECT id,name,fid,node_level,path_info,term FROM " + self.table + \
                  " WHERE name='{0}' AND term={1} ORDER BY node_level DESC".format(name, term)
        else:
            sql = "SELECT id,name,fid,node_level,path_info,term FROM " + self.table + \
                  " WHERE name='{0}' ORDER BY node_level DESC".format(name)
        course = self.execute_sql_with_one_data(sql)
        return course

    def query_course_by_name_fid(self, name, fid):
        sql = "SELECT id,name,fid,node_level,path_info,term,sort FROM "+self.table+\
                  " WHERE name='{0}' AND fid={1} ORDER BY node_level DESC".format(name, fid)
        course = self.execute_sql_with_one_data(sql)
        return course

    def query_course_by_name_level(self, name, level, fid=None):
        if fid is not None:
            sql = "SELECT id,name,fid,node_level,path_info,term,sort FROM " + self.table + \
                  " WHERE name='{0}' AND node_level={1} AND fid = {2} ORDER BY node_level DESC".format(name, level, fid)
        else:
            sql = "SELECT id,name,fid,node_level,path_info,term,sort FROM "+self.table+\
                  " WHERE name='{0}' AND node_level={1} ORDER BY node_level DESC".format(name, level)
        course = self.execute_sql_with_one_data(sql)
        return course

    def query_name_remark(self, size=1000):
        sql = "SELECT id,name,name_remark FROM " + self.table + " WHERE " \
                                    " name_remark IS NOT NULL and name_remark<>''"

        data = self.execute_sql_with_many_data(sql, size=size)
        return data

    def query_course_list(self, id):
        sql = "SELECT a.fid,a.id,b.name AS chapter_name,a.name_remark,a.name FROM " + self.table + \
              " AS a left join " + self.table + " AS b ON a.fid = b.id WHERE a.id = {0}".format(id)
        data = self.execute_sql_with_one_data(sql)
        return data

    def stat_course_by_name_level(self, name, level, fid):
        total = 0
        sql = "SELECT count(id) AS total FROM "+self.table+" WHERE name='{0}' AND node_level={1} AND fid = {2}".format(name, level, fid)
        result = self.execute_sql_with_one_data(sql)
        if result is not None:
            total = result[0]
        return total

    def stat_by_level(self, level):
        total = 0
        sql = "SELECT count(id) AS total FROM " + self.table + " WHERE node_level={0}".format(level)
        result = self.execute_sql_with_one_data(sql)
        if result is not None:
            total = result[0]
        return total

    def stat_course_by_name(self, name):
        total = 0
        sql = "SELECT count(id) AS total FROM "+self.table+" WHERE name='{0}'".format(name)
        result = self.execute_sql_with_one_data(sql)
        if result is not None:
            total = result[0]
        return total

    def update_status_by_id(self, id, status):
        sql = "UPDATE " + self.table + " SET status={0} WHERE id={1}".format(status, id)
        # print(sql)
        self.execute_sql_without_data(sql)

    def update_course_path_by_id(self, id, path):
        sql = "UPDATE "+self.table+" SET path_info='{0}' WHERE id={1}".format(path, id)
        self.execute_sql_without_data(sql)

    def update_course_level_by_id(self, id, level):
        sql = 'UPDATE '+self.table+' SET node_level={0} WHERE id={1}'.format(level, id)
        self.execute_sql_without_data(sql)

    def update_course_sort_by_id(self, id):
        sql = 'UPDATE '+self.table+' SET sort={0} WHERE id={1}'.format(id, id)
        self.execute_sql_without_data(sql)

    def update_course_by_name_remark(self, id, remark):
        sql = "UPDATE " + self.table + " SET name_remark='{0}' WHERE id={1}".format(remark, id)
        self.execute_sql_without_data(sql)

    def query_course_by_level(self, level):
        sql = "SELECT id,name,fid,node_level,term FROM "+self.table+" WHERE node_level={0} AND term>0".format(level)
        data = self.execute_sql_with_many_data(sql, 10000)
        return data

    def update_course_fid(self, id, fid):
        sql = "UPDATE " + self.table + " SET fid={0} WHERE id={1}".format(fid, id)
        self.execute_sql_without_data(sql)

    def delete_course(self, id):
        sql = "DELETE FROM "+self.table+" WHERE id={0}".format(id)
        self.execute_sql_without_data(sql)

    def query_course_by_node_level(self, level):
        sql = "SELECT id,name,path_info,term FROM tb_course_structure_tree where node_level=" + level
        print(sql)
        data = self.execute_sql_with_many_data(sql, 1000)
        return data

    def query_course_structure_by_path(self, path_info):
        sql = "SELECT b.id as chapter_id,a.id,c.name as class_name,b.name AS chapter_name,a.name " \
              "FROM tb_course_structure_tree AS a" \
              " LEFT JOIN tb_course_structure_tree AS b ON a.fid=b.id LEFT JOIN tb_course_structure_tree AS c ON" \
              " c.id=b.fid where a.path_info like '"+path_info+"%' and a.node_level=6 order by a.id asc"
        # print(sql)
        data = self.execute_sql_with_many_data(sql, 1000)
        return data

    def query_course_by_path(self, path_info):
        sql = "select id,name,node_level,path_info from tb_course_structure_tree where path_info like '"\
              + path_info + "%' order by id asc"
        data = self.execute_sql_with_many_data(sql, 10000)
        return data

    def close(self):
        self.cursor.close()
        self.connect.close()


# 华师大章节
class ChapterMySql(MySql):
    def __init__(self,  host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def query_by_name(self, name):
        sql = "SELECT _id,grade,name FROM " + self.table + " WHERE replace(`name`,' ','') ='{0}'".format(name)
        data = self.execute_sql_with_one_data(sql)
        return data

    def query_by_parent(self, id):
        sql = "SELECT _id,grade,replace(`name`,' ','') FROM " + self.table + " WHERE parent='{0}'".format(id)
        data = self.execute_sql_with_many_data(sql, 1000)
        return data

    def stat_children(self, id):
        total = 0
        sql = "SELECT count(_id) AS total FROM " + self.table + " WHERE parent='{0}'".format(id)
        data = self.execute_sql_with_one_data(sql)
        if data is not None:
            total = data[0]
        return total

    def export_data(self):
        sql = "SELECT c.name AS chapter_name, b.name AS section_name, a.name,a.`grade`,a.`gradeNumber`,a.`_id` " \
              "FROM tb_hsd_chapter AS a LEFT JOIN tb_hsd_chapter AS b ON a.`parent`=b.`_id` " \
              "LEFT JOIN tb_hsd_chapter AS c ON b.`parent`=c.`_id` " \
              "WHERE a.gradeNumber>0 AND (a.`parent` IS NOT NULL AND a.`parent`<>'') ORDER BY a.gradeNumber ASC"
        data = self.execute_sql_with_many_data(sql, 50000)
        return data

    def not_video_data(self, video_table):
        sql = " SELECT c.name AS chapter_name, b.name AS section_name, a.name,a.`grade`,a.`gradeNumber`,a.`_id` FROM "+\
              self.table +" AS a LEFT JOIN " + self.table + " AS b ON a.`parent`=b.`_id` LEFT JOIN "+\
              self.table +" AS c ON b.`parent`=c.`_id` WHERE a.gradeNumber>0 AND " \
                          "(a.`parent` IS NOT NULL AND a.`parent`<>'') " \
                          "AND a._id NOT IN (SELECT forein_question_chapter FROM " +\
              video_table + " ) ORDER BY a.gradeNumber ASC"
        data = self.execute_sql_with_many_data(sql, 50000)
        return data


# 华师大题目
class QuestionMySql(MySql):

    def __init__(self, host, user, passwd, port, db, charset, table):
            MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def stat_question_by_chapter(self, chapter):
        total = 0
        sql = "SELECT count(*) AS total FROM " + self.table + " WHERE chapter='{0}'".format(chapter)
        result = self.execute_sql_with_one_data(sql)
        if result is not None:
            total = result[0]
        return total

    def total_stat_question_by_chapters(self, chapters):
        total = 0
        result = self.stat_question_by_chapters(chapters)
        if result is not None:
            totals = result.values()
            for v in totals:
                total += v
        return total

    def stat_question_by_chapters(self, chapters):
        totals = {}
        lists = []
        for c in chapters:
            lists.append("'" + c + "'")
        sql = "SELECT chapter,count(*) AS total FROM tb_hsd_question WHERE " \
                "chapter IN (" + ",".join(lists) + ") GROUP BY chapter"
        result = self.execute_sql_with_many_data(sql, 50000)
        if result is not None:
            for r in result:
                totals.setdefault(r[0], r[1])

        return totals


# 研究性
class ResearchMySql(MySql):
    def __init__(self, host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def query_by_name(self, name):
        sql = "SELECT id,name FROM " + self.table + " WHERE name='{0}'".format(name)
        data = self.execute_sql_with_one_data(sql)
        return data

    def insert_data(self, name):
        sql = "INSERT INTO "+ self.table +\
              "(name,remark) VALUES('{0}','{1}')".format(name, name)
        id = self.execute_sql_with_id(sql)
        return id


# 名校
class SchoolMySql(MySql):

    def __init__(self, host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def add_school(self, school_dict):
        sql = "INSERT INTO " + self.table + "(name) VALUES('{0}')".format(school_dict['name'])
        id = self.execute_sql_with_id(sql)
        return id

    def query_school_by_name(self, name):
        sql = "SELECT id,name FROM " + self.table + " WHERE name='{0}'".format(name)
        data = self.execute_sql_with_one_data(sql)
        return data


# 名师
class TeacherMySql(MySql):

    def __init__(self, host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def add_teacher(self, teacher_dict):
        sql = "INSERT INTO " + self.table + \
              "(name) VALUES('{0}')".format(teacher_dict['name'])
        id = self.execute_sql_with_id(sql)
        return id

    def query_teacher_by_name(self, name):
        sql = "SELECT id,name,remark FROM " + self.table + " WHERE name='{0}'".format(name)
        teacher = self.execute_sql_with_one_data(sql)
        return teacher


# 视频
class VideoMySql(MySql):

    def __init__(self,  host, user, passwd, port, db, charset, table):
        MySql.__init__(self, host, user, passwd, port, db, charset, table)

    def insert_video_by_full(self, video_dict):
        id = 0
        sql = "INSERT INTO " + self.table + \
              "(`foreign_course_property`,`bestbox3_origin_name`,`origin_name`,`video_short_url`,`show_name`,`foreign_course_structure_tree`," \
              "`full_url`,`status`,`ocn_status`, `group_asset_id`,`video_asset_id`,`video_md5` ,`call_back_series_no` ,`call_back_asset_id` ," \
              "`sort`,`remark`) " \
              "VALUES ({0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')".format(
                  video_dict[0], video_dict[1], video_dict[2], video_dict[3], video_dict[4], video_dict[5], pymysql.escape_string(video_dict[6]), video_dict[7],
                   video_dict[8], video_dict[9], video_dict[10], video_dict[11], video_dict[12], video_dict[13], video_dict[14], video_dict[15])
        # print(sql)
        id = self.execute_sql_with_id(sql)
        return id

    def insert_video(self, video_dict):
        sql = "INSERT INTO "+self.table+\
              "(foreign_course_structure_tree,foreign_course_property,bestbox3_origin_name,show_name,foreign_school," \
              "foreign_teacher,award_resource,foreign_reasearch_based) " \
              "VALUES ('{0}','{1}','{2}','{3}',{4},{5},{6},{7})".format(
            video_dict['foreign_course_structure_tree'], video_dict['foreign_course_property'], video_dict['bestbox3_origin_name'],
            pymysql.escape_string(video_dict['show_name']), video_dict['foreign_school'], video_dict['foreign_teacher'],
            video_dict['award_resource'], video_dict['foreign_reasearch_based'])
        id = self.execute_sql_with_id(sql)
        return id

    def insert_video_by_short(self, video_dict):
        sql = "INSERT INTO " + self.table + \
              "(foreign_course_structure_tree,foreign_course_property,bestbox3_origin_name,origin_name,show_name,status,ocn_status) " \
              "VALUES ({0},{1},'{2}','{3}','{4}',{5},{6})".format(
                  video_dict['foreign_course_structure_tree'], video_dict['foreign_course_property'],
                  video_dict['bestbox3_origin_name'], video_dict['origin_name'],
                  pymysql.escape_string(video_dict['show_name']), 1, 0)
        id = self.execute_sql_with_id(sql)
        return id

    def stat_video(self, course):
        total = 0
        sql = "SELECT count(*) AS total FROM "+self.table+" WHERE foreign_course_structure_tree={0}".format(course)
        result = self.execute_sql_with_one_data(sql)
        if result is not None:
            total = result[0]
        return total

    # 通过名称进行判断
    def query_video_by_bestbox_origin_name(self, name):
        sql = "SELECT * FROM " + self.table + "  WHERE bestbox3_origin_name='{0}'".format(name)
        data = self.execute_sql_with_one_data(sql)
        return data

    def query_video_by_short_url(self, file):
        sql = "SELECT * FROM " + self.table + " WHERE video_short_url='{0}'".format(file)
        data = self.execute_sql_with_one_data(sql)
        return data

    def query_video_by_name(self, name):
        sql = "SELECT * FROM " + self.table + " WHERE show_name='{0}'".format(name)
        data = self.execute_sql_with_one_data(sql)
        return data

    def query_data_by_course(self, course, size=10000):
        sql = "SELECT `foreign_course_property`,`bestbox3_origin_name`,`origin_name`,`video_short_url`,`show_name`,`foreign_course_structure_tree`," \
              "`full_url`," \
              "`status`,`ocn_status`, `group_asset_id`,`video_asset_id`,`video_md5` ,`call_back_series_no` ,`call_back_asset_id` ," \
              "`sort`,`remark` FROM " + self.table + " WHERE " \
              "foreign_course_structure_tree={0}".format(course)
        # print(sql)
        data = self.execute_sql_with_many_data(sql, size=size)
        return data

    def query_data(self, size=100):
        sql = "SELECT id,foreign_course_structure_tree,show_name,forein_question_chapter FROM " + self.table + " WHERE" \
              " (forein_question_chapter IS NULL OR forein_question_chapter='') AND foreign_course_structure_tree>0"
        data = self.execute_sql_with_many_data(sql, size=size)
        return data

    def update_foreign(self, id, course):
        sql = "UPDATE " + self.table + " set foreign_course_structure_tree='{0}' WHERE id={1}".format(course, id)
        self.execute_sql_without_data(sql)
        return True

    def update_by_question_chapter(self, id, chapter):
        sql = "UPDATE " + self.table + " set forein_question_chapter='{0}' WHERE id={1}".format(chapter, id)
        self.execute_sql_without_data(sql)

    def stat_video_data(self, course_id):
        total = 0
        sql = "SELECT count(foreign_course_structure_tree) as total  FROM " + self.table + " WHERE foreign_course_structure_tree = "\
              + course_id+" group by foreign_course_structure_tree order by total asc"
        data = self.execute_sql_with_one_data(sql)
        if data is not None:
            total = data[0]
        return total

    def export_data(self, course_table, video_table):
        sql = "SELECT a.fid as chapter_id,a.id,b.name AS chapter_name,a.name FROM " \
              "" + course_table+" AS a LEFT JOIN " + course_table + " AS b ON a.fid=b.id WHERE a.id IN " \
              "(SELECT foreign_course_structure_tree FROM " + video_table + " WHERE " \
              "forein_question_chapter IS NOT NULL AND forein_question_chapter<>'')"
        data = self.execute_sql_with_many_data(sql, 50000)
        return data

    def no_question_data(self, course_table, video_table):
        sql = "SELECT a.fid as chapter_id,a.id,b.name AS chapter_name,a.name FROM " \
              "" + course_table + " AS a LEFT JOIN " + course_table + " AS b ON a.fid=b.id WHERE a.id IN " \
                                "(SELECT foreign_course_structure_tree FROM " + video_table + " WHERE " \
                                "forein_question_chapter IS NULL OR forein_question_chapter='') AND a.node_level=7"
        data = self.execute_sql_with_many_data(sql, 50000)
        return data

    def query_question_id_by_course(self, course_id):
        questions = []
        sql = "SELECT forein_question_chapter FROM " + self.table + \
              " WHERE foreign_course_structure_tree={0} AND forein_question_chapter IS NOT NULL " \
              "AND forein_question_chapter<>'' GROUP BY forein_question_chapter".format(course_id)
        data = self.execute_sql_with_many_data(sql, 50000)
        if data is not None:
            for i in data:
                questions.append(i[0])
        return questions

