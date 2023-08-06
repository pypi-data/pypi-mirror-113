import os
from threading import Thread
from multiprocessing import cpu_count
from queue import *


def worker_def(A):
    q = A[0]
    while True:
        item = q.get()
        if item is None:
            break
        else:
            file = item
            os.remove(file)
            q.task_done()


def delete_files_in_path(path):
    thread_count = int(cpu_count()*0.8)
    q = Queue(maxsize=thread_count)
    A = (q,)
    threads = []
    for worker in range(thread_count):
        t = Thread(target=worker_def, args=(A,))
        t.start()
        threads.append(t)
    for file in os.listdir(path):
        q.put(os.path.join(path, file))
    for i in range(thread_count):
        q.put(None)
    for t in threads:
        t.join()
    return None


def delete_everything_down_path(path):
    for root, directories, files in os.walk(path):
        if files:
            delete_files_in_path(root)
        for directory in directories:
            delete_everything_down_path(os.path.join(root, directory))
            os.removedirs(os.path.join(root, directory))
    return None


if __name__ == '__main__':
    pass
