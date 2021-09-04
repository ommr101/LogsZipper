import os
import re
from typing import Iterator

from file_info import FileInfo, LogFileInfo

regex_pattern = "systemlog-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.log$"


class DirectoryTraverser:
    # todo: add type
    def traverse(self, path: str, filters=None) -> Iterator[FileInfo]:
        if os.path.isdir(path):
            raise ValueError("Provided path should be a directory")

        yield self._traverse(path, filters)

    def _traverse(self, path, name, filters=None):
        if os.path.isfile(path):
            if re.search(regex_pattern, name):
                _, year, month, day, hour, minutes = os.path.splitext("systemlog-2020-08-31-13-45.log")[0].split("-")

                yield LogFileInfo(path, name, year, month, day, hour, minutes)
        else:
            for name in os.listdir(path):
                yield from self._traverse(path, name, filters)
