from multiprocessing import Process, Queue

from file_info import LogFileInfo
from traverser import DirectoryTraverser
from zipper import Zipper

input_dir = r"C:\Users\User\PycharmProjects\LogsZipper\test\input"
output_dir = r"C:\Users\User\PycharmProjects\LogsZipper\test\ouptput"


def traverser_worker(queue: Queue):
    traverser: DirectoryTraverser = DirectoryTraverser()
    for file_info in traverser.traverse(input_dir):
        queue.put(file_info)


def zipper_worker(queue: Queue):
    zipper: Zipper = Zipper(output_dir)
    while True:
        file_info: LogFileInfo = queue.get()
        zipper.zip(file_info)


if __name__ == '__main__':
    q = Queue()

    zipper_worker_process = Process(target=zipper_worker, args=(q,))
    traverser_worker_process = Process(target=traverser_worker, args=(q,))

    zipper_worker_process.start()
    traverser_worker_process.start()

    traverser_worker_process.join()
    zipper_worker_process.join()
