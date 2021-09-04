from file_info import FileInfo


class Zipper:
    def __init__(self, directory: str):
        self.directory = directory

    def zip(self, file_info: FileInfo):
        print(file_info.path)
