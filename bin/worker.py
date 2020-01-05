from multiprocessing import Process
from multiprocessing import Queue
import time
import os


class Worker(Process):

    def __init__(self, interval, path, handler, pip_conn):
        Process.__init__(self)
        self.interval = interval
        self.close_interval = 3
        self.queue_handler = Queue()
        self._init_data(path)
        self.handler = handler
        self.pip_conn = pip_conn

    def _init_data(self, path):
        inode = os.stat(path).st_ino
        file_metadata = {
            'path': path,
            'inode': inode,
            'file_path': path,
            'counter': 0,
            'last_time': 0,
            'size': 0,
        }
        self.queue_handler.put(file_metadata)
        self.file_metadata = file_metadata

    def run(self):

        path = self.file_metadata['path']
        inode = os.stat(path).st_ino
        with open(path, mode='r', encoding='utf-8') as fd:
            while True:
                content = fd.readline()
                str_len = len(content)
                if str_len > 0:
                     self.handler.parse(content)
                     self._update_queue_size(inode, str_len)
                     self.pip_conn.send(str_len)
                else:
                    self._update_queue_counter(inode, 1)
                    if self.file_metadata['counter'] > self.close_interval:
                        self.pip_conn.send(0)
                        #break 通知Manage进程 让其定时 到一定时刻重新打开
                time.sleep(self.interval)

    def _update_queue_size(self, inode, size):
        item = self.queue_handler.get()
        if item['inode'] == inode:
            item['size'] += size
            item['last_time'] = time.time()
            self.queue_handler.put(item)
        self.file_metadata = item

    def _update_queue_counter(self, inode, step):
        item = self.queue_handler.get()

        if item['inode'] == inode:
            item['counter'] += step
            item['last_time'] = time.time()
            self.queue_handler.put(item)
        self.file_metadata = item