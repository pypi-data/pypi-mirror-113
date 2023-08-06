import functools
import os
from enum import Enum
from os import stat_result
from typing import BinaryIO, Generator, List, TextIO, Union


class StorageEngine:
    """
    StorageEngine implements interface for storage engines and default behaviour for some methods.
    Key method is `open()`. If storage engine implements `open()`, some of
    these methods will be working in default behaviour (e.g. `download_to_file` will read using
    implemented `open()` method and write to physical drive).
    See help(StorageEngine.__init__)
    """

    class Filter(Enum):
        """
        File-directory filter for `list` method.
        """

        DIR = 1
        FILE = 2
        DIR_AND_FILE = 3

    class Hash(Enum):
        """
        Names-constants of hash methods, which may be used in Storage Engine hashsum methods.
        """

        MD5 = 1
        CRC = 2
        SHA_256 = 3
        SHA_512 = 4
        SHA3 = 5

    def assert_file(function):
        """
        Checks, whether first argument of decorated function is path to a file.
        :raise FileNotFoundError:
        """

        @functools.wraps(function)
        def wrapper(self, path, *args, **kwargs):
            self.check_no_prefix_slash_path(path)
            if not self.is_file(path):
                raise FileNotFoundError(f"File `{path}` does not exists.")
            return function(self, path, *args, **kwargs)

        return wrapper

    def assert_directory(function):
        """
        Checks, whether first argument of decorated function is path to a dictionary.
        :raise NotADirectoryError:
        """

        @functools.wraps(function)
        def wrapper(self, path, *args, **kwargs):
            self.check_no_prefix_slash_path(path)
            if not self.is_dir(path):
                raise NotADirectoryError(f"Directory `{path}` does not exists.")
            return function(self, path, *args, **kwargs)

        return wrapper

    def assert_file_or_directory(function):
        """
        Asserts that first argument of decorated function is path to file or directory.
        :raise FileNotFoundError:
        """

        @functools.wraps(function)
        def wrapper(self, path, *args, **kwargs):
            self.check_no_prefix_slash_path(path)
            if not (self.is_file(path) or self.is_dir(path)):
                raise FileNotFoundError(f"Item `{path}` is neither file, nor directory.")
            return function(self, path, *args, **kwargs)

        return wrapper

    def assert_not_directory(function):
        """
        Checks, whether first argument of decorated function is not a path to a dictionary.
        :raise FileExistsError: if path is path to a directory
        """

        @functools.wraps(function)
        def wrapper(self, path, *args, **kwargs):
            self.check_no_prefix_slash_path(path)
            if self.is_dir(path):
                raise FileExistsError(f"Path `{path}` is a directory.")
            return function(self, path, *args, **kwargs)

        return wrapper

    def check_no_prefix_slash_path(self, path) -> None:
        if path.startswith("/"):
            raise ValueError(f"Storage engine paths can't start with `/` symbol.")

    def check_not_empty_path(self, path) -> None:
        if path == "":
            raise FileNotFoundError(f"Path can't be empty.")

    def check_no_dot_path(self, path) -> None:
        patterns = ["/../", "/./", "../", "/.."]
        bad_paths = [".."]
        for pattern in patterns:
            if pattern in path:
                raise ValueError(f"Path can't contain `{pattern}`.")
        for bad_path in bad_paths:
            if bad_path == path:
                raise ValueError(f"Path can't be `{bad_path}`.")

    def __init__(self, link: str = None, cache_path: str = None, other: dict = None, remote: dict = None):
        """
        See StorageEngine.__doc__
        :param link: path to folder, where files are stored (mounting point)
        :param cache_path: path to folder, where files can be cached
        :param other: dictionary with additional arguments
        :param remote: dictionary with remote (cloud) connection details
        """
        self._link = link
        self._cache_path = cache_path
        self._other = other
        self._remote = remote

    def delete(self, filepath: str) -> None:
        """
        Removes file.
        If cache is used, you may also remove recursively all empty parent directories from `filepath`.
        :raise FileNotFoundError: if file does not exists
        :raise IsADirectoryError: if object is directory and not file
        """
        raise NotImplementedError

    def rmdir(self, dirpath: str) -> None:
        """
        Removes empty directory.
        :raise FileNotFoundError: if directory does not exists
        :raise OSError: if directory is not empty
        """
        raise NotImplementedError

    def rmtree(self, dirpath: str) -> None:
        """
        Removes directory recursively.
        :raise FileNotFoundError: if directory does not exists
        """
        raise NotImplementedError

    def size(self, path: str) -> int:
        """
        :return: size of file (for directory it is zero constant).
        :raise FileNotFoundError: if object does not exists
        """
        raise NotImplementedError

    def stat(self, path: str) -> stat_result:
        """
        :return: stat details for file system object
        :raise: FileNotFoundError: if object does not exists
        """
        raise NotImplementedError

    def join(self, path: str, *paths: str) -> str:
        """
        Joins paths to one path. Default implementation uses os.path's join.
        Used for joining storage engine's paths.
        TODO: this method is probably useless, as storage engine methods although expects,
        that remote and local paths are separated by slash symbol...
        """
        return os.path.join(path, *paths)

    def get_hashsum(self, filepath: str, hash_type: Enum = Hash.MD5) -> bytes:
        """
        Get hash sum of `filepath`.
        :param filepath: path to file, whose hash sum is to be returned
        :param hash_type: hash function to be used. See `help(StorageEngine.Hash)` enum. Default is MD5.
        :return: binary string with hashsum
        :raise FileNotFoundError: if file does not exists
        """
        raise NotImplementedError

    def get_local_hashsum(self, filepath: str, hash_type: Enum = Hash.MD5) -> bytes:
        """
        Get hash sum of currently cached version of `filepath` (if caching is supported).
        :param filepath: path to file, whose hash sum is to be returned
        :param hash_type: hash function to be used. See `help(StorageEngine.Hash)` enum. Default is MD5.
        :return: binary string with hashsum
        :raise FileNotFoundError: if file does not exists
        """
        raise NotImplementedError

    def exists(self, path: str) -> bool:
        """
        :return: true, if file system object (file or directory) exists.
        :raise FileNotFoundError: if object does not exists
        """
        raise NotImplementedError

    def is_file(self, filepath: str) -> bool:
        """
        :return: True, if `filepath` is path to a file. False otherwise.
        """
        raise NotImplementedError

    def is_dir(self, dirpath: str) -> bool:
        """
        :return: True, if 'dirpath' is path to directory. False otherwise.
        """
        raise NotImplementedError

    def mkdir(self, dir_name: str, mode=None) -> None:
        """
        Creates directory.
        :raise FileExistsError: if directory already exists
        :raise FileNotFoundError: if some directory within dirpath does not exists
        """
        raise NotImplementedError

    def mkdirs(self, dirpath: str, mode=None, exist_ok=False) -> None:
        """
        Creates directory recursively.
        :param exist_ok: if False, a FileExistsError is raised if the target directory already exists
        """
        raise NotImplementedError

    def mkfile(self, filepath: str) -> None:
        """
        Creates empty file.
        :raise FileExistsError: if file already exists
        """
        self.open(filepath, "x").close()

    def open(self, filepath: str, mode: str = "r", *args, **kwargs) -> Union[TextIO, BinaryIO]:
        """
        Opens file and returns it's file pointer.
        :raise FileNotFoundError: if file does not exists
        :raise OSError: if file can't be opened
        """
        raise NotImplementedError

    def get_local_path(self, path: str) -> str:
        """
        Returns path to local copy of remote `path`, if `path` is in cache and also in cloud.
        Useful for cloud storage engines, which uses cache. Remote `path` may be file or directory.
        If file, this copy is not supposed to be actual version of remote file.
        If no such file in cache or in cloud, returns empty string.
        This method should raise ValueError, if path starts with slash (not allowed).
        :return: absolute path to local copy of remote `path`. If no such object in cache (or file not on cloud),
        returns empty string.
        """
        raise NotImplementedError

    def _create_local_filepath(self, filepath: str, replace_existing: bool = True) -> str:
        """
        Creates and returns absolute path for remote file `filepath` in cache.
        If `filepath` contains directories, which do not exists yet, this method will create them. File name should
        be intact, only appended at the end of final string.
        If there are name conflcts, especially when:
         1) some of directories in `filepath` are file objects on local drive
         2) or file with that path exists in cache
         remove them (it), if `replace_existing` is set to True (default). If False, raise FileExistsError.
        This method should not check, whether file exists on cloud.
        This method should raise ValueError, if path starts with slash (not allowed).
        Example:
        >>>_create_local_filepath("path/within/cloud/file")
        >>>"/cache/path/path/within/cloud/file"
        :return: absolute cache path corresponding to `filepath`
        :raise FileExistsError:
        :raise ValueError:
        """
        raise NotImplementedError

    def _create_local_dirpath(self, dirpath: str, replace_existing: bool = True) -> str:
        """
        Creates and returns absolute path for remote directory `dirpath` in cache.
        If `dirpath` contains directories, which do not exists yet, this method will create them.
        If there are name conflcts (some of directories in `filepath` are file objects on local drive)
        remove them if `replace_existing` is set to True (default). If False, raise FileExistsError.
        This method should not check, whether directory exists on cloud.
        This method should raise ValueError, if path starts with slash (not allowed).
        Example:
        >>>_create_local_dirpath("path/within/cloud/folder")
        >>>"/cache/path/path/within/cloud/folder"
        :return: absolute cache path corresponding to `dirpath`
        :raise FileExistsError: see above
        :raise ValueError:
        """
        raise NotImplementedError

    def list_directory(self, dirpath: str) -> List[str]:
        """
        Lists directory, non recursively. This method together with `_recursive_directory_list_generator`
        implements recursive `list()` method.
        """
        raise NotImplementedError

    def _recursive_directory_list_generator(
        self, base, depth, filter: Enum = Filter.DIR_AND_FILE, infix: str = ""
    ) -> Generator:
        """
        Traverse `base` path to depth, and yields item names (file and directories) according to filter.
        Stops if there are no more items or when `depth` is reached.
        """
        if depth < 1:
            yield from []
        else:
            for item_path in self.list_directory(self.join(base, infix)):
                item_path = self.join(infix, item_path)
                item_base_path = self.join(base, item_path)
                if self.is_file(item_base_path) and (filter == self.Filter.FILE or filter == self.Filter.DIR_AND_FILE):
                    yield item_path
                elif self.is_dir(item_base_path):
                    if filter == self.Filter.DIR or filter == self.Filter.DIR_AND_FILE:
                        yield item_path
                    yield from self._recursive_directory_list_generator(base, depth - 1, filter, item_path)

    @assert_directory
    def list(self, dirpath: str, filter: Enum = Filter.DIR_AND_FILE, depth: int = 1) -> List[str]:
        """
        Returns list of file system object names (files, directories). If depth > 1, lists also
        objects in directories to depth (e.g. if depth=2, list also directories in `dirpath`).
        Records from sub-directories will be prefixed with their path, relative to `dirpath`.
        :param filter: directories, files or both (default). See StorageEngine.Filter enum.
        :param depth: max dept to which subdirectories will be listed (default is 1, only current directory)
        :return: list of file system object names in current directory (and recursive, if depth > 1)
        :raise NotADirectoryError: if directory does not exists
        """
        return list(self._recursive_directory_list_generator(dirpath, depth, filter))

    @assert_file
    def read_as_text(self, filepath: str) -> str:
        """
        :return: content of file in string
        :raise FileNotFoundError: if file does not exists
        """
        return self.open(filepath, "r").read()

    @assert_file
    def read_as_bytes(self, filepath: str) -> bytes:
        """
        :return: content of file in bytes
        :raise FileNotFoundError: if file does not exists
        """
        return self.open(filepath, "rb").read()

    @assert_file
    def download_to_file(self, filepath: str, local_path: str = None, exist_ok: bool = True) -> None:
        """
        Downloads file and writes it to 'local_path'.
        If storage is local (not cloud), download means copy (copy from `filepath` to `local_path`)
        :param local_path: path to directory or path to file, where remote file will be written.
            1) If `local_path` is None, remote file will be downloaded to cache folder
            (if cache is supported, otherwise NotImplementedError will be raised.
            2) If `local_path` is directory, file name from `filepath` will be appended
        :raise FileExistsError: if exists_ok is False, and local_file exists (or exists_ok is False and name of the
        file to be downloaded exists in local_dir)
        :raise FileNotFoundError: if 'filepath' does not exists, or if local_path contains directories, which
        does not exist
        """
        if local_path is None:
            local_path = self._create_local_filepath(filepath)
        elif os.path.isdir(local_path):
            local_path = os.path.join(local_path, os.path.basename(filepath))
        if exist_ok is False and os.path.isfile(local_path):
            raise FileExistsError(f"File `{os.path.basename(local_path)}` already exists.")
        with open(local_path, "wb") as out_file:
            in_file = self.open(filepath, "rb")
            out_file.write(in_file.read())
            in_file.close()

    @assert_not_directory
    def upload_from_file(self, filepath: str, local_filepath: str) -> None:
        """
        Writes file from local_filepath to filepath.
        If storage is local (not cloud), upload means copy (copy from `local_file` to `filepath`)
        :raise FileNotExistsError: if 'local_filepath' does not exists
        """
        with open(local_filepath, "rb") as in_file:
            out_file = self.open(filepath, "wb")
            out_file.write(in_file.read())
            out_file.close()

    @assert_not_directory
    def write_as_text(self, filepath: str, content: str) -> None:
        """
        Writes `content` (string) to file in `filepath`
        """
        file = self.open(filepath, "w")
        file.write(content)
        file.close()

    @assert_not_directory
    def write_as_bytes(self, filepath: str, content: bytes) -> None:
        """
        Writes `content` (binary data) to file in `filepath`
        """
        file = self.open(filepath, "wb")
        file.write(content)
        file.close()

    def remove_cache_dir(self, dirpath: str, recursive: bool = False) -> None:
        """
        Removes directory `dirpath` from cache. If `recursive` is true, remove also files and sub-directories.
        Otherwise raise OSError if `dirpath` is not empty.
        :raise OSError:
        :raise NotADirectoryError:
        """
        raise NotImplementedError

    def remove_cache(self) -> None:
        """
        Remove all items from cache.
        """
        raise NotImplementedError

    def remove_cache_object(self, path: str) -> None:
        """
        Removes object with path `path` from cache no matter if object is file, directory (empty or non-empty) or
        even if object does not exists.
        """
        raise NotImplementedError
