class FileInfo:
    def __init__(self, path: str, name: str):
        self.path: str = path
        self.name: str = name


class LogFileInfo(FileInfo):
    def __init__(self, path: str, name: str, year: str, month: str, day: str, hour: str, min: str):
        super().__init__(path, name)
        self.path: str = path
        self.name: str = name
        self.year: str = year
        self.month: str = month
        self.day: str = day
        self.hour: str = hour
        self.min: str = min
