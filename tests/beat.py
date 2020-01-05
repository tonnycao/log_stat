
import os
import time
import queue
from bin.worker import Worker
from hander.hander_nginx import HanderNginx
from multiprocessing import Pipe

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/access.log'
qname = 'file_queue'
target = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/target.log'


def init_data(queue_handle, path):
    inode = os.stat(path).st_ino
    file_metadata = {
        'inode': inode,
        'file_path': path,
        'counter': 0,
        'last_time': 0,
        'size': 0,
    }
    queue_handle.put(file_metadata)
    return file_metadata


def update_queue_size(queue_handler, inode, size):
    '''
    更新传输大小
    :param queue_handler:
    :param inode:
    :param size:
    :return:
    '''
    item = queue_handler.get()
    if item['inode'] == inode:
        item['size'] += size
        item['last_time'] = time.time()
        queue_handler.put(item)


def update_queue_counter(queue_handler, inode, step):
    '''
    更新停动次数
    :param queue_handler:
    :param inode:
    :param step:
    :return:
    '''
    item = queue_handler.get()

    if item['inode'] == inode:
        item['counter'] += step
        item['last_time'] = time.time()
        queue_handler.put(item)


def read_file(queue_handler, path, target):
    inode = os.stat(path).st_ino
    with open(path, mode='r', encoding='utf-8') as fd:
        while True:
            content = fd.readline()
            str_len = len(content)
            if str_len > 0:
                with open(target, mode='a+', encoding='utf-8') as fd2:
                    fd2.write(content+"\n")
                    update_queue_size(queue_handler, inode, str_len)
            else:
                update_queue_counter(queue_handler, inode, 1)
            time.sleep(2)

def main():
    q = queue.Queue()
    init_data(q, file_path)
    read_file(q, file_path, target)


if __name__ == '__main__':
    reader = []
    parent_conn, child_conn = Pipe()

    nginx_handler = HanderNginx(target)
    p = Worker(2, file_path, nginx_handler, child_conn)
    p.start()
    reader.append(parent_conn)

    while True:
        for i in reader:
            print(
                i.recv()
            )
            if i.recv() == 0:
                p.join(10)