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
        size = 0
        try:
            last_size = self.pip_conn.recv()
            if last_size[2] > 0:
                size = last_size[2]
        except:
            pass

        file_metadata = {
            'path': path,
            'inode': inode,
            'file_path': path,
            'counter': 0,
            'last_time': 0,
            'size': size,
        }
        self.queue_handler.put(file_metadata)
        self.file_metadata = file_metadata

    def run(self):

        path = self.file_metadata['path']
        inode = os.stat(path).st_ino
        with open(path, mode='r', encoding='utf-8') as fd:
            while True:
                if fd.seekable():
                    fd.seek(self.file_metadata['size'])
                content = fd.readline()
                str_len = len(content)
                if str_len > 0:
                     self.handler.parse(content)
                     self._update_queue_size(inode, str_len)
                     tup = (path, inode, str_len)
                     self.pip_conn.send(tup)
                else:
                    self._update_queue_counter(inode, 1)
                    if self.file_metadata['counter'] > self.close_interval:
                        self.pip_conn.send((path, inode, 0))
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