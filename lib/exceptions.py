# 自定义异常类
from config.config import *


class MyExcept(Exception):
    '''
    常见做法定义异常基类,然后在派生不同类型的异常
    '''

    def __init__(self, *args):
        self.args = args


class DropDataaseError(MyExcept):
    def __init__(self):
        self.args = ('删除数据库错误!',)
        self.message = '删除数据库错误!'
        self.code = 100


class DropTableError(MyExcept):
    def __init__(self):
        self.args = ('删除表错误!',)
        self.message = '删除表错误！'
        self.code = 200


class CreateDatabaseError(MyExcept):
    def __init__(self):
        self.args = ('不能创建数据库',)
        self.message = '不能创建数据库'
        self.code = 300


class OperatorError(MyExcept):
    '''
    操作错误,一般是要做的事情和实际功能不匹配
    '''

    def __init__(self, message):
        self.args = (message,)
        self.message = message
        self.code = 400


class FileIsExistsError(MyExcept):
    def __init__(self, message):
        self.args = (message,)
        self.message = message
        self.code = 500