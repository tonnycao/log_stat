import string
from config.config import *
from lib.mysql import ChapterMySql
from lib.mysql import VideoMySql
from lib.mysql import CourseMySql

course_db = CourseMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_tmp_course_structure_tree')

chapter_db = ChapterMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_hsd_chapter')

video_db = VideoMySql(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PWD, port=MYSQL_PORT, db=MYSQL_DB,
                    charset=MYSQL_CHARSET, table='tb_tmp_course_video_detail_bak'
)


videos = video_db.query_data(5000)
stat = 0
total = 0
chapters = set()
chapter_total = 0
for video in videos:
    courses = course_db.query_course_list(video[1])
    if courses is not None:
        # 章
        chapter = chapter_db.query_by_name(courses[2])
        if chapter is not None:
            total += 1
            # 节
            sections = chapter_db.query_by_parent(chapter[0])
            if sections is not None:
                for section in sections:
                    # 判断是否是末节点
                    total = chapter_db.stat_children(section[0])
                    if total == 0:
                        chapters.add(section[2])
                        chapter_total += 1
                        if section[2] == courses[4]:
                            # 知识点匹配
                            video_db.update_by_question_chapter(video[0], section[0])
                            stat += 1
                        elif section[2] == courses[3]:
                            # 章节匹配
                            video_db.update_by_question_chapter(video[0], section[0])
                            stat += 1
                        else:
                            # 处理异常字符后是否匹配
                            tmp = section[2].strip(string.digits)
                            tmp = tmp.strip('.')
                            chapter_name = tmp.strip(string.digits)
                            if chapter_name == courses[3]:
                                video_db.update_by_question_chapter(video[0], section[0])
                                stat += 1
                            elif chapter_name == courses[4]:
                                video_db.update_by_question_chapter(video[0], section[0])
                                stat += 1
                    else:
                        points = chapter_db.query_by_parent(section[0])
                        # 知识点
                        if points is not None:
                            for point in points:
                                total = chapter_db.stat_children(point[0])
                                if total == 0:
                                    chapters.add(point[2])
                                    chapter_total += 1
                                    if point[2] == courses[4]:
                                        video_db.update_by_question_chapter(video[0], point[0])
                                        stat += 1
                                    elif point[2] == courses[3]:
                                        video_db.update_by_question_chapter(video[0], point[0])
                                        stat += 1
                                    else:
                                        tmp = point[2].strip(string.digits)
                                        tmp = tmp.strip('.')
                                        chapter_name = tmp.strip(string.digits)
                                        if chapter_name == courses[3]:
                                            video_db.update_by_question_chapter(video[0], point[0])
                                            stat += 1
                                        elif chapter_name == courses[4]:
                                            video_db.update_by_question_chapter(video[0], point[0])
                                            stat += 1
                                else:
                                    children = chapter_db.query_by_parent(point[0])
                                    if children is not None:
                                        for child in children:
                                            chapters.add(child[2])
                                            chapter_total += 1
                                            if child[2] == courses[4]:
                                                video_db.update_by_question_chapter(video[0], child[0])
                                                stat += 1
                                            elif child[2] == courses[3]:
                                                video_db.update_by_question_chapter(video[0], child[0])
                                                stat += 1
                                            else:
                                                tmp = child[2].strip(string.digits)
                                                tmp = tmp.strip('.')
                                                chapter_name = tmp.strip(string.digits)
                                                if chapter_name == courses[3]:
                                                    video_db.update_by_question_chapter(video[0], child[0])
                                                    stat += 1
                                                elif chapter_name == courses[4]:
                                                    video_db.update_by_question_chapter(video[0], child[0])
                                                    stat += 1



