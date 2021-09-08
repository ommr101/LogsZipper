import os
import queue
from multiprocessing import Lock, Process, Queue
from typing import List
from zipfile import ZipFile

import config
from file_info import LogFileInfo


class Zipper:
    def __init__(self, output_dir: str, files_info: Queue, workers: int = 1):
        if not os.path.isdir(output_dir):
            raise ValueError(f"The path {output_dir} is not a directory")

        self._output_dir: str = output_dir
        self._files_info: Queue = files_info

        self._workers_quantity: int = workers
        self._workers: List[ZipperWorker] = []

        self._create_date_directory_lock: Lock = Lock()
        self._write_zip_lock: Lock = Lock()

    def start(self) -> None:
        for _ in range(self._workers_quantity):
            searcher_worker: ZipperWorker = ZipperWorker(self._output_dir, self._files_info,
                                                         self._create_date_directory_lock, self._write_zip_lock)
            searcher_worker.start()
            self._workers.append(searcher_worker)

    def join(self) -> None:
        for w in self._workers:
            w.join()


class ZipperWorker(Process):
    def __init__(self, output_dir: str, files_info: Queue, create_date_directory_lock: Lock(), write_zip_lock: Lock()):
        super().__init__()

        self._output_dir: str = output_dir
        self._files_info: Queue = files_info

        self._create_date_directory_lock: Lock = create_date_directory_lock
        self._write_zip_lock: Lock = write_zip_lock

        self._is_done: bool = False

    def run(self) -> None:
        while not self._is_done:
            try:
                self._zip()
            except queue.Empty:
                print(f"Process {self.name} timed out on waiting for files to zip")
                self._is_done = True

    def _zip(self) -> None:
        file_info: LogFileInfo = self._files_info.get(timeout=config.GET_QUEUE_TIMEOUT)
        date_output_dir: str = os.path.join(self._output_dir, file_info.get_date())

        if not os.path.exists(date_output_dir):
            with self._create_date_directory_lock:
                if not os.path.exists(date_output_dir):
                    os.mkdir(date_output_dir)

        files_zip_name: str = file_info.get_zipped_name() + '.zip'
        files_zip_path: str = os.path.join(date_output_dir, files_zip_name)

        with self._write_zip_lock:
            with ZipFile(files_zip_path, 'a') as files_zip:
                files_zip.write(file_info.path, file_info.name)