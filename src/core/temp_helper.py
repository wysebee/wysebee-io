import glob
import os
import tempfile
from typing import List
from .filesystem import create_directory, move_file, remove_directory
from .singleton import singleton

@singleton
class TempFileHelper:

    def get_temp_file_path(self, file_path: str) -> str:
        _, temp_file_extension = os.path.splitext(os.path.basename(file_path))
        temp_directory_path = self.get_temp_directory_path(file_path)
        return os.path.join(temp_directory_path, "temp" + temp_file_extension)

    def move_temp_file(self, file_path: str, move_path: str) -> bool:
        temp_file_path = self.get_temp_file_path(file_path)
        return move_file(temp_file_path, move_path)

    def get_base_directory_path(self) -> str:
        return os.path.join(tempfile.gettempdir(), self._folderName)

    def create_base_directory(self, folderName = "app") -> bool:
        self._folderName = folderName
        base_directory_path = self.get_base_directory_path()
        return create_directory(base_directory_path)

    def clear_base_directory(self) -> bool:
        base_directory_path = self.get_base_directory_path()
        return remove_directory(base_directory_path)

    def get_temp_directory_path(self, file_path: str) -> str:
        temp_file_name, _ = os.path.splitext(os.path.basename(file_path))
        base_directory_path = self.get_base_directory_path()
        return os.path.join(base_directory_path, temp_file_name)

    def create_temp_directory(self, file_path: str) -> bool:
        temp_directory_path = self.get_temp_directory_path(file_path)
        return create_directory(temp_directory_path)

    def clear_temp_directory(self, file_path: str) -> bool:
        temp_directory_path = self.get_temp_directory_path(file_path)
        return remove_directory(temp_directory_path)
