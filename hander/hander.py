# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 10:34
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : handler.py
# @Software: PyCharm
import abc


class Hander(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse(self):
        pass

    @abc.abstractmethod
    def notify(self):
        pass