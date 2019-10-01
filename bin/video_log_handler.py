# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 15:59
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : video_log_handler.py
# @Software: PyCharm

import os
import time
from config.config import *


def stat_video_log(log_file):
    '''
    解析文件，获取文件名
    :param log_file:
    :return: []
    '''

    data = set()
    fd = open(log_file, 'r', encoding='utf-8')
    for line in fd.readlines():
        if len(line) > 0:
            line = line.strip()
            content = line.split(',')
            if len(content) > 4 and content[4] is not None:
                contents = content[4].split(':')
                data.add(contents[1])
    return data


def stat_video_dir(path):
    '''
    遍历目录下所有文件
    :param path:
    :return:list 文件列表
    '''

    # root当前根目录 dirs目录列表 files 文件列表
    files_list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            files_list.append(file_path)

    return files_list


def main(path, out_file):
    '''
     主函数
    :param path:
    :param out_file:
    :return:void
    '''

    names_list = set()
    files = stat_video_dir(path)

    if len(files) > 0:
        for log in files:
            result = stat_video_log(log)
            for name in result:
                names_list.add(name)

    if len(names_list) > 0:
        fd = open(out_file, mode='a+', encoding='utf-8')
        for i in names_list:
            fd.write(i+'\n')
        fd.close()


if __name__ == '__main__':
    start_time = time.time()
    log_path = DATA_PATH + '/alter'
    file = DATA_PATH + '/vo.log'
    main(log_path, file)
    end_time = time.time()
    span_time = end_time - end_time
    print('span time:' + str(span_time))