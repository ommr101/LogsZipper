import os
import re
from typing import Iterator

from file_info import LogFileInfo, FileInfoFactory

regex_pattern = "systemlog-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.log$"


class DirectoryTraverser:
    # todo: add type
    def traverse(self, path: str) -> Iterator[LogFileInfo]:
        if os.path.isfile(path):
            file_name = os.path.basename(path)
            file_info = FileInfoFactory.create(path, file_name)
            if file_info:
                yield file_info
        else:
            for name in os.listdir(path):
                next_path = os.path.join(path, name)
                yield from self.traverse(next_path)

