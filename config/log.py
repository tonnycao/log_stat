# -*- coding: utf-8 -*-
# @Time    : 2019/7/26 13:50
# @Author  : Tonny Cao
# @Email   : 647812411@qq.com
# @File    : log.py
# @Software: PyCharm

import logging
import logging.config

# # create logger
logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug

ch = logging.FileHandler(filename='log.log', encoding='utf-8')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')


# logging.config.fileConfig('logging.conf')
#
# # create logger
# logger = logging.getLogger('root')
#
# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')