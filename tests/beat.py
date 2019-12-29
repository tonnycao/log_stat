
import os
import time
import queue

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
    queue_handle.put(qname, file_metadata)
    return file_metadata


def update_queue(queue_handler, inode, size):
    item = queue_handler.get(qname)
    print(item)
    print('sss')
    if item.inode == inode:
        item.size += size
        item.last_time = time.time()
        queue_handler.put(item)


def read_file(queue_handler, path, target):
    inode = os.stat(path).st_ino
    with open(path, mode='r', encoding='utf-8') as fd:
        while True:
            content = fd.readline(1)
            str_len = len(content)
            if str_len > 0:
                with open(target, mode='w+', encoding='utf-8') as fd2:
                    fd2.write(content+"\n")
                    update_queue(queue_handler, inode, str_len)
            time.sleep(2)

def main():
    q = queue.Queue()
    init_data(q, file_path)
    read_file(q, file_path, target)


if __name__ == '__main__':
    main()
