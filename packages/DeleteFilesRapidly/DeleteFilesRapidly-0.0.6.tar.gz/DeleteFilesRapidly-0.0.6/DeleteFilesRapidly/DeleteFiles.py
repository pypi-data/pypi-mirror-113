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


class DeleteEverythingDownPath(object):
    def __init__(self, path):
        thread_count = int(cpu_count() * 0.8)
        self.q = Queue(maxsize=thread_count)
        A = (self.q,)
        threads = []
        for worker in range(thread_count):
            t = Thread(target=worker_def, args=(A,))
            t.start()
            threads.append(t)
        self.delete_everything_down_path(path=path)
        for i in range(thread_count):
            self.q.put(None)
        for t in threads:
            t.join()

    def delete_everything_down_path(self, path):
        for root, directories, files in os.walk(path):
            for file in files:
                self.q.put(os.path.join(root, file))
            for directory in directories:
                self.delete_everything_down_path(os.path.join(root, directory))
                os.rmdir(os.path.join(root, directory))


if __name__ == '__main__':
    pass
