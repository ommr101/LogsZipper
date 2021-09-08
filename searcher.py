import os
import queue
from multiprocessing import Queue, Process, Value
from typing import List

import config
from file_info import FileInfoFactory


class Searcher:
    def __init__(self, input_dir, files_info: Queue, workers: int = 1):
        if not os.path.isdir(input_dir):
            raise ValueError(f"The path {input_dir} is not a directory")

        self._workers_quantity = workers

        self._files_info: Queue = files_info

        self._directories_path: Queue = Queue()
        self._directories_path.put((input_dir, 0))

        self._workers: List[DirectorySearcher] = []

    def start(self):
        for _ in range(self._workers_quantity):
            searcher_worker: DirectorySearcher = DirectorySearcher(self._directories_path, self._files_info)
            searcher_worker.start()
            self._workers.append(searcher_worker)

    def join(self):
        for w in self._workers:
            w.join()


class DirectorySearcher(Process):
    def __init__(self, directories_path: Queue, files_queue: Queue):
        super().__init__()

        self._files_queue: Queue = files_queue
        self._directories_path: queue = directories_path

        self._is_done: bool = False

    def run(self):
        while not self._is_done:
            try:
                self._traverse()
            except queue.Empty:
                print(f"Process {self.name} timed out on waiting for paths to traverse")
                self._is_done = True

    def _traverse(self) -> None:
        path, depth = self._directories_path.get(timeout=config.GET_QUEUE_TIMEOUT)
        if os.path.isfile(path):
            file_name = os.path.basename(path)
            file_info = FileInfoFactory.create(path, file_name)
            if file_info:
                self._files_queue.put(file_info)
        else:
            depth += 1

            if depth <= config.MAX_DEPTH_LEVEL:
                for name in os.listdir(path):
                    next_path = os.path.join(path, name)
                    self._directories_path.put((next_path, depth))
