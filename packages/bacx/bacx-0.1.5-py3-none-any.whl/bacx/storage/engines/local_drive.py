import functools
import hashlib
import os
import shutil
from enum import Enum
from os import stat_result
from typing import BinaryIO, Generator, List, TextIO, Union

from bacx.storage.engines.engine import StorageEngine


class LocalDrive(StorageEngine):
    """
    LocalDrive is storage engine, which resides on your physical drive, in `link` directory.
    Basically, it is wrapper for Python's builtin open() method.
    For details, about it's methods see help(LocalDrive) and help(StorageEngine).
    """

    def __init__(self, link: str = None, cache_path: str = None, other: dict = None, remote: dict = None):
        """See LocalDrive.__doc__ and StorageEngine.__doc__"""
        if not isinstance(link, str):
            raise TypeError(f"LocalDrive requires `link` argument to be a string path to base directory.")
        if not os.path.isdir(link):
            raise NotADirectoryError(f"Provided path to base directory (`link`) does not exists (got: `{link}`)")
        super().__init__(link=link, cache_path=cache_path, other=other, remote=remote)

    def get_real_path(self, path):
        """
        Path used by user is always relative to base directory, and target file must be inside base directory.
        Therefore path can't starts with `/`, can't contain `/../` and must starts with `link`.
        :return: `path` prefixed with path to base directory (`link`)
        """
        if path.startswith("/"):
            raise ValueError(f"LocalDrive path can't starts with `/`. " f"Path is always relative to base directory")
        path = os.path.join(self._link, path)
        if "/../" in path:
            raise ValueError(f"LocalDrive does not allow using super directory (`/../`).")
        return path

    def open(self, filepath, *args, **kwargs) -> Union[TextIO, BinaryIO]:
        return open(self.get_real_path(filepath), *args, **kwargs)

    def get_local_path(self, path: str) -> str:
        return self.get_real_path(path) if self.is_file(path) else ""

    def mkdir(self, dir_name: str, mode=0o777) -> None:
        return os.mkdir(self.get_real_path(dir_name), mode)

    def mkdirs(self, dirpath: str, mode=0o777, exist_ok=False) -> None:
        return os.makedirs(self.get_real_path(dirpath), mode, exist_ok)

    def is_file(self, filepath: str) -> bool:
        return os.path.isfile(self.get_real_path(filepath))

    def is_dir(self, dirpath: str) -> bool:
        return os.path.isdir(self.get_real_path(dirpath))

    def exists(self, path: str) -> bool:
        return self.is_dir(path) or self.is_file(path)

    @StorageEngine.assert_file
    def get_hashsum(self, filepath: str, hash_type: Enum = StorageEngine.Hash.MD5) -> bytes:
        if hash_type != StorageEngine.Hash.MD5:
            raise NotImplementedError(f"Only MD5 hash function is supported")
        filepath = self.get_real_path(filepath)
        with open(filepath, "rb") as file:
            return hashlib.md5(file.read()).digest()

    def list_directory(self, dirpath: str) -> List[str]:
        return os.listdir(self.get_real_path(dirpath))

    @StorageEngine.assert_file_or_directory
    def stat(self, path: str) -> stat_result:
        return os.stat(self.get_real_path(path))

    @StorageEngine.assert_file_or_directory
    def size(self, path: str) -> int:
        return os.path.getsize(self.get_real_path(path))

    @StorageEngine.assert_directory
    def rmtree(self, dirpath: str) -> None:
        return shutil.rmtree(self.get_real_path(dirpath))

    @StorageEngine.assert_directory
    def rmdir(self, dirpath: str) -> None:
        if len(self.list(dirpath)) > 0:
            raise OSError(f"Directory `{dirpath}` is not empty.")
        return os.rmdir(self.get_real_path(dirpath))

    @StorageEngine.assert_file
    def delete(self, filepath: str) -> None:
        return os.remove(self.get_real_path(filepath))
