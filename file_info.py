import os
import re

from abc import ABC, abstractmethod
from typing import Optional


class FileInfo(ABC):
    @abstractmethod
    def __init__(self, path: str, name: str):
        self.path: str = path
        self.name: str = name

    @staticmethod
    @abstractmethod
    def regex_pattern() -> str:
        raise NotImplementedError

    @abstractmethod
    def get_date(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_zipped_name(self) -> str:
        raise NotImplementedError


class LogFileInfo(FileInfo):
    def __init__(self, path: str, name: str):
        super().__init__(path, name)

        _, self._year, self._month, self._day, self._hour, _ = os.path.splitext(name)[0].split("-")

    @staticmethod
    def regex_pattern() -> str:
        return r"systemlog-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.log$"

    def get_date(self) -> str:
        return '-'.join([self._year, self._month, self._day])

    def get_zipped_name(self) -> str:
        return '-'.join(['systemlog', self.get_date(), self._hour])


class FileInfoFactory:
    @staticmethod
    def create(file_path: str, file_name: str) -> Optional[FileInfo]:
        if re.search(LogFileInfo.regex_pattern(), file_name):
            return LogFileInfo(file_path, file_name)

        return None
