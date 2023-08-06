import base64
import binascii
import os
from enum import Enum
from typing import List

from google.cloud import storage

from bacx.storage.engines.cloud_engine import CloudStorageEngine
from bacx.storage.engines.engine import StorageEngine


class GcloudDrive(CloudStorageEngine):
    """
    Google cloud storage connector's implementation comes from AwsDrive implementation. For more information
    see AwsDrive docstrings.
    """

    def __init__(self, *args, **kwargs):
        """
        See help(GcloudDrive) and help(CloudStorageEngine) or help(StorageEngine)
        """
        super().__init__(*args, **kwargs)
        if self._other is not None and "key_path" in self._other:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self._other["key_path"]
        self._gcloud = storage.Client()
        self._bucket = self._gcloud.bucket(self._link)

    def _normalize_directory_path(self, dirpath: str) -> str:
        return "" if dirpath == "" else f"{dirpath.rstrip('/')}/"

    def optional_file_path_check(self, path) -> None:
        if path.endswith("/"):
            raise ValueError(f"File name can't end with `/` symbol.")
        if self.is_dir(path):
            raise IsADirectoryError(f"Path `{path}` is a directory.")
        if "/" in path and not self.is_dir(path.rsplit("/", 1)[0]):
            raise NotADirectoryError(f"Path `{path.rsplit('/', 1)[0]}` is not a directory.")

    @StorageEngine.assert_file
    def delete(self, filepath: str) -> None:
        self._bucket.blob(filepath).delete()
        self.remove_cache_object(filepath)

    @StorageEngine.assert_directory
    def rmdir(self, dirpath: str) -> None:
        if self.list_directory(dirpath):
            raise OSError(f"Directory `{dirpath}` is not empty.")
        dirpath = self._normalize_directory_path(dirpath)
        self._bucket.blob(dirpath).delete()
        self.remove_cache_object(dirpath)

    @StorageEngine.assert_directory
    def rmtree(self, dirpath: str) -> None:
        dirpath = self._normalize_directory_path(dirpath)
        for blob in self._gcloud.list_blobs(self._link, prefix=dirpath):
            blob.delete()
        self.remove_cache_object(dirpath)

    @StorageEngine.assert_file_or_directory
    def size(self, path: str) -> int:
        if self.is_dir(path):
            path = self._normalize_directory_path(path)
        if path == "":
            return 0
        blob = self._bucket.blob(path)
        blob.reload()
        return blob.size

    def exists(self, path: str) -> bool:
        return self.is_file(path) or self.is_dir(path)

    def is_file(self, filepath: str) -> bool:
        if filepath.endswith("/") or filepath == "":
            return False
        blob = self._bucket.blob(filepath)
        return blob.exists() and not self.is_dir(f"{filepath}")

    def is_dir(self, dirpath: str) -> bool:
        if dirpath == "":
            return True
        dirpath = self._normalize_directory_path(dirpath)
        blob = self._bucket.blob(dirpath)
        if not blob.exists():
            return False
        blob.reload()
        return blob.size == 0

    @CloudStorageEngine.assert_normalized_path
    def mkdir(self, dir_name: str, mode=None) -> None:
        dir_name = self._normalize_directory_path(dir_name)
        if self.is_dir(dir_name):
            raise IsADirectoryError(f"Directory `{dir_name}` already exists.")
        if self.is_file(dir_name[:-1]):
            raise FileExistsError(f"File `{dir_name[:-1]}` already exists.")
        dir_list = dir_name[:-1].rsplit("/", 1)
        if len(dir_list) > 1:
            if self.is_file(dir_list[0]):
                raise FileExistsError(f"Path `{dir_list[0]}` is a file.")
            if not self.is_dir(dir_list[0]):
                raise FileNotFoundError(f"Path `{dir_list[0]}` is not a directory.")
        self._bucket.blob(dir_name).upload_from_string("")

    @CloudStorageEngine.assert_normalized_path
    def mkdirs(self, dirpath: str, mode=None, exist_ok=False) -> None:
        """
        exists_ok is ignored, as `dirpath` must be absolute and therefore we don't know
        which path of provided path should be checked
        """
        path_list = dirpath.split("/")
        path = ""
        for item in path_list:
            path = os.path.join(path, item)
            if not self.is_dir(path):
                self.mkdir(path)

    @StorageEngine.assert_directory
    def list_directory(self, dirpath: str) -> List[str]:
        dirpath = self._normalize_directory_path(dirpath)
        pref_len = len(dirpath)
        items = [item.name for item in self._gcloud.list_blobs(self._link, prefix=dirpath)]
        result = []
        for item in items:
            if len(item) > pref_len:
                item = item[pref_len:]
                item = item.split("/", 1)[0]
                if item not in result and item != "":
                    result.append(item)
        return result

    @StorageEngine.assert_file
    def get_hashsum(self, remote_path: str, hash_type: Enum = StorageEngine.Hash.MD5) -> bytes:
        file = self._bucket.blob(remote_path)
        file.reload()
        return binascii.hexlify(base64.decodebytes(file.md5_hash.encode("utf-8"))).decode("ascii")

    def _upload_file(self, remote_path: str, local_path: str, *args, **kwargs) -> None:
        self.optional_file_path_check(remote_path)
        self._bucket.blob(remote_path).upload_from_filename(local_path)

    @StorageEngine.assert_file
    def _download_file(self, remote_path: str, local_path: str, *args, **kwargs) -> None:
        self.optional_file_path_check(remote_path)
        self._bucket.blob(remote_path).download_to_filename(local_path)
