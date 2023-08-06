import functools
import hashlib
import os
import shutil
from enum import Enum
from typing import BinaryIO, TextIO, Union

from bacx.storage.engines.engine import StorageEngine
from bacx.storage.engines.local_drive import LocalDrive


class CloudStorageEngine(StorageEngine):
    """
    CloudStorageEngine is abstract (super) class for StorageEngines, which needs caching functionality (mostly
    cloud storage engines).

    For basic functionality, cloud storage engine needs to implement:
        `_upload_file`, `_download_file`, `is_file`, `is_dir`, `list_directory` and `get_hashsum` methods.
    For full storage engine functionality, all `StorageEngine` abstract methods needs to be implemented (see
    docstrings in `StorageEngine` to implement this methods as it is expected).

    Important note: if you will be implementing methods, which change remote filesystem (mostly `delete`, `rmdir`,
    `rmtree`, `mkdir` and `mkdirs`) do not forget to make the same changes in cache (`open` and `mkfile` are already
    implemented). Access to cache is handled via CloudStorageEngine's private `LocalDrive` (see `LocalDrive` for
    more details). Basically, for example if you are implementing `rmdir`, then after successful remove operation
    on remote cloud, you will need to call self._cache.rmdir("folder/in/cache")`.

    Additional notes:
    Do not forget to use assert decorators. They raise exceptions with correct messages.

    See also help(StorageEngine). Docstrings for overriden methods are in `StorageEngine` class.
    """

    def assert_normalized_path(function):
        """
        Checks, whether first argument of decorated function (path) satisfy required conditions.
        This checks are primary due to cache, as some patterns in path may results in unwanted behaviour
        (reading/writing out of cache folder).
        :raise FileNotFoundError:
        :raise ValueError:
        """

        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            if len(args) == 0 and len(kwargs) == 0:
                raise AttributeError(f"Decorated function is expected to take at least one argument.")
            path = args[0] if len(args) > 0 else next(iter(kwargs.values()))
            self.check_not_empty_path(path)
            self.check_no_prefix_slash_path(path)
            self.check_no_dot_path(path)
            return function(self, *args, **kwargs)

        return wrapper

    def optional_file_path_check(self, path) -> None:
        """
        This method is callback, which is called by CloudStorageEngine's `open()` method before
        open operations are performed. Override this method to perform additional checks on `path` argument.
        :param path: path to be used by `open()` method
        """
        pass

    def __init__(self, *args, **kwargs):
        """
        See help(CloudStorageEngine) and help(StorageEngine)
        :param cache_folder: path to a local folder, where files can be stored.
        """
        super().__init__(*args, **kwargs)
        if not isinstance(self._cache_path, str):
            raise ValueError(
                f"Cloud storage engine constructor requires " f"`cache_path` argument to be path to cache folder."
            )
        self._cache = LocalDrive(link=self._cache_path)

    def _upload_file(self, remote_path: str, local_path: str, *args, **kwargs) -> None:
        """
        Uploads file from `local_path` to remote `filepath`.
        :param args: additional arguments
        :param kwargs: additional arguments
        """
        raise NotImplementedError

    @StorageEngine.assert_file
    def _download_file(self, remote_path: str, local_path: str, *args, **kwargs) -> None:
        """
        Downloads file from remote `filepath` to `filepath`.
        :param args: additional arguments
        :param kwargs: additional arguments
        """
        raise NotImplementedError

    @StorageEngine.assert_file
    def get_hashsum(self, remote_path: str, hash_type: Enum = StorageEngine.Hash.MD5) -> bytes:
        raise NotImplementedError

    @staticmethod
    def hook_file_close(file, callback, *args, close_first: bool = True, **kwargs):
        """
        Hooks `callback` call to `close()` method of given `file`.
        :param args: arguments for `callback`
        :param close_first: call `callback` after or before file `close()`.
        If True (default), then when `file.close()` will be called, file will be closed and then callback
        will be called. If False, callback will be called before file close.
        :param kwargs: key-value arguments for `callback`
        :return: original `file` with modified `close()` method.
        """
        original_close = file.close

        def new_close(*orig_args, **orig_kwargs):
            if close_first:
                original_close(*orig_args, **orig_kwargs)
                return callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)
                return original_close(*orig_args, **orig_kwargs)

        file.close = new_close
        return file

    @StorageEngine.assert_file
    def get_local_hashsum(self, filepath: str, hash_type: Enum = StorageEngine.Hash.MD5) -> str:
        """
        Note: return value is changed from bytes to str (i don't know how to convert aws_drive's md5 sum
        from string to digest().... You can fix it.)
        """
        if hash_type != StorageEngine.Hash.MD5:
            raise NotImplementedError(f"Only MD5 hash function is supported")
        cached_path = self.get_local_path(filepath)
        if cached_path == "":
            raise FileNotFoundError(f"File `{filepath}` is not in cache.")
        with open(cached_path, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()

    def _open_from_cache(self, local_path: str, remote_path: str, *args, **kwargs) -> Union[TextIO, BinaryIO]:
        """
        Opens file in `local_path` and returns it's file pointer. When `close()` method is called on
        this file pointer, content of file will be uploaded to `filepath`.
        :return: file pointer
        """
        file = open(local_path, *args, **kwargs)
        self.hook_file_close(file, self._upload_file, remote_path, local_path)
        return file

    @assert_normalized_path
    def get_local_path(self, path: str) -> str:
        if not self.is_dir(path) and not self.is_file(path):
            return ""
        cached_path = os.path.join(self._cache_path, path)
        if os.path.isfile(cached_path) or os.path.isdir(cached_path):
            return cached_path
        else:
            return ""

    @assert_normalized_path
    def _create_local_filepath(self, filepath: str, replace_existing: bool = True) -> str:
        dir_path = os.path.dirname(filepath)
        dir_path = self._create_local_dirpath(dir_path, replace_existing) if dir_path != "" else self._cache_path
        final_path = os.path.join(dir_path, os.path.basename(filepath))
        # final_path still may be existing file or directory:
        if os.path.isdir(final_path) and replace_existing:
            shutil.rmtree(final_path)
        elif os.path.isdir(final_path):
            raise FileExistsError(f"Could not create file `{filepath}` in cache: `{final_path}` is a directory.")
        elif os.path.isfile(final_path) and replace_existing:
            os.remove(final_path)
        elif os.path.isfile(final_path):
            raise FileExistsError(f"Could not create file `{filepath}` in cache: file `{final_path}` exists.")
        return final_path

    @assert_normalized_path
    def _create_local_dirpath(self, dirpath: str, replace_existing: bool = True) -> str:
        build_path = self._cache_path
        directories = list(filter(bool, dirpath.split("/")))
        for directory in directories:
            build_path = os.path.join(build_path, directory)
            if os.path.isdir(build_path):
                continue
            if os.path.isfile(build_path) and replace_existing:
                os.remove(build_path)
            elif os.path.isfile(build_path):
                raise FileExistsError(f"Could not create directory `{dirpath}` in cache: `{build_path}` is a file.")
            build_path = os.path.join(self._cache_path, dirpath)
            break
        if not os.path.isdir(build_path):
            os.makedirs(build_path)
        elif os.path.isdir(build_path) and replace_existing:
            shutil.rmtree(build_path)
            os.mkdir(build_path)
        else:
            raise FileExistsError(f"Could not create directory `{dirpath}` in cache: `{build_path}` is a file.")
        return build_path

    @assert_normalized_path
    def remove_cache_dir(self, dirpath: str, recursive: bool = False) -> None:
        if recursive:
            self._cache.rmtree(dirpath)
        else:
            self._cache.rmdir(dirpath)

    def remove_cache(self) -> None:
        for item in self._cache.list("."):
            if self._cache.is_file(item):
                self._cache.delete(item)
            else:
                self._cache.rmtree(item)

    @assert_normalized_path
    def remove_cache_object(self, path: str) -> None:
        if self._cache.is_file(path):
            self._cache.delete(path)
        elif self._cache.is_dir(path):
            self._cache.rmtree(path)

    def open(self, filepath: str, mode: str = "r", *args, **kwargs) -> Union[TextIO, BinaryIO]:
        """
        Opens remote file `filepath` from updated file cache version.
        :param filepath: remote path to file
        :param mode: open mode
        :return: file pointer
        """
        self.optional_file_path_check(filepath)
        # get cache path to this remote file:
        cached_path = self.get_local_path(filepath)
        if cached_path == "":
            # file is not in cache. Create new cache path for this file. Download if file, except case, that
            # file mode is crate or write:
            cached_path = self._create_local_filepath(filepath)
            if "x" not in mode and "w" not in mode:
                self._download_file(filepath, cached_path)
        elif self.get_hashsum(filepath, StorageEngine.Hash.MD5) != self.get_local_hashsum(
            filepath, StorageEngine.Hash.MD5
        ):
            # hash not equal, download new file version:
            self._download_file(filepath, cached_path)
        return self._open_from_cache(cached_path, filepath, mode, *args, **kwargs)
