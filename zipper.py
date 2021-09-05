import os
import zipfile
from zipfile import ZipFile

from file_info import LogFileInfo


class Zipper:
    def __init__(self, directory: str):
        self.directory = directory
        if not os.path.exists(directory):
            raise ValueError("The given directory does not exist")
        if not os.path.isdir(directory):
            raise ValueError("The given directory path is not a directory")

    def zip(self, file_info: LogFileInfo):
        date_directory = os.path.join(self.directory, file_info.get_date())
        if not os.path.exists(date_directory):
            os.mkdir(date_directory)

        files_zip_name = file_info.get_zipped_name() + '.zip'
        files_zip_path = os.path.join(date_directory, files_zip_name)

        with ZipFile(files_zip_path, 'a', zipfile.ZIP_DEFLATED) as files_zip:
            files_zip.write(file_info.path, file_info.name)