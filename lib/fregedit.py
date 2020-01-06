# -*- coding: utf-8 -*-
# @Time    : 2020/1/6 14:09
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : fregedit.py
# @Software: PyCharm
import sqlite3

class Fregedit(object):

    def __init__(self):
        self._create_db()

    def _create_db(self):
        conn = sqlite3.connect('file_regedit.db')
        self._conn = conn
        c = conn.cursor()
        self._cursor = c
        files_sql = "CREATE TABLE watch_files" \
              "(ip text, path text, name text, inode INTEGER, size INTEGER, counter INTEGER, last_time text)"
        self._cursor.execute(files_sql)
        self._cursor.close()
