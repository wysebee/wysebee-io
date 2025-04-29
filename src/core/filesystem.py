import os
import shutil
from pathlib import Path
from typing import List, Optional

def get_file_size(file_path : str) -> int:
	if is_file(file_path):
		return os.path.getsize(file_path)
	return 0


def same_file_extension(file_paths : List[str]) -> bool:
	file_extensions : List[str] = []

	for file_path in file_paths:
		_, file_extension = os.path.splitext(file_path.lower())

		if file_extensions and file_extension not in file_extensions:
			return False
		file_extensions.append(file_extension)
	return True


def is_file(file_path : str) -> bool:
	return bool(file_path and os.path.isfile(file_path))


def is_directory(directory_path : str) -> bool:
	return bool(directory_path and os.path.isdir(directory_path))


def in_directory(file_path : str) -> bool:
	if file_path and not is_directory(file_path):
		return is_directory(os.path.dirname(file_path))
	return False

def resolve_relative_path(path : str) -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def copy_file(file_path : str, move_path : str) -> bool:
	if is_file(file_path):
		shutil.copy(file_path, move_path)
		return is_file(move_path)
	return False


def move_file(file_path : str, move_path : str) -> bool:
	if is_file(file_path):
		shutil.move(file_path, move_path)
		return not is_file(file_path) and is_file(move_path)
	return False


def remove_file(file_path : str) -> bool:
	if is_file(file_path):
		os.remove(file_path)
		return not is_file(file_path)
	return False


def create_directory(directory_path : str) -> bool:
	if directory_path and not is_file(directory_path):
		Path(directory_path).mkdir(parents = True, exist_ok = True)
		return is_directory(directory_path)
	return False


def list_directory(directory_path : str) -> Optional[List[str]]:
	if is_directory(directory_path):
		files = os.listdir(directory_path)
		files = [ Path(file).stem for file in files if not Path(file).stem.startswith(('.', '__')) ]
		return sorted(files)
	return None


def remove_directory(directory_path : str) -> bool:
	if is_directory(directory_path):
		shutil.rmtree(directory_path, ignore_errors = True)
		return not is_directory(directory_path)
	return False
