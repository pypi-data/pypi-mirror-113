import os.path
import time
from enum import Enum
from typing import List

import boto3
import botocore

from bacx.storage.engines.cloud_engine import CloudStorageEngine
from bacx.storage.engines.engine import StorageEngine


class AwsDrive(CloudStorageEngine):
    """
    This implementation of StorageEngine Aws boto3 connector makes some restrictions on objects (files and folders)
    stored on Aws boto3. First of all, Aws boto3 is a flat file system, which means, that there are actually
    no folders. There are just object's with some size and key. This key may be interpreted as a path, although
    it does not works like path on classic file system. Because StorageEngine integrates different storages,
    objects stored on Aws boto3 accessed by this connector are interpreted by this way:
    Path (boto3 `Key`) can be a file if:
        - does not ends with `/`
        - directory with the same name and suffix `/` does not exists (e.g. `name` and `name/`)
        - is zero or nonzero size
    Path (boto3 `Key`) can be a directory if:
        - ends with `/`
        - file with the same name and without suffix `/` does not exists (e.g. `name/` and `name`)
        - parent in it's path is a directory
        - must be a zero size
    Root directory is empty string ""
    Path (boto3 `Key`), which ends with `/`, and whose object's size is nonzero can't be accessed,
    and can't be used within StorageEngine's path (although such object can exists on Aws boto3).
    """

    def __init__(self, *args, **kwargs):
        """
        See help(AwsDrive) and help(CloudStorageEngine) or help(StorageEngine)
        """
        super().__init__(*args, **kwargs)
        if self._other is not None and "key_id" in self._other and "key" in self._other:
            self._aws = boto3.client(
                "s3", aws_access_key_id=self._other["key_id"], aws_secret_access_key=self._other["key"]
            )
        else:
            self._aws = boto3.client("s3")

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
        self._aws.delete_object(Bucket=self._link, Key=filepath)
        self.remove_cache_object(filepath)

    @StorageEngine.assert_directory
    def rmdir(self, dirpath: str) -> None:
        if self.list_directory(dirpath):
            raise OSError(f"Directory `{dirpath}` is not empty.")
        dirpath = self._normalize_directory_path(dirpath)
        self._aws.delete_object(Bucket=self._link, Key=dirpath)
        self.remove_cache_object(dirpath)

    @StorageEngine.assert_directory
    def rmtree(self, dirpath: str) -> None:
        dirpath = self._normalize_directory_path(dirpath)
        self.remove_cache_object(dirpath)
        dir_content = self._aws.list_objects_v2(Bucket=self._link, Prefix=dirpath)["Contents"]
        # TODO: may be speed-up using delete_objects()
        for item in dir_content:
            self._aws.delete_object(Bucket=self._link, Key=item["Key"])

    @StorageEngine.assert_file_or_directory
    def size(self, path: str) -> int:
        if self.is_dir(path):
            path = self._normalize_directory_path(path)
        return 0 if path == "" else self._aws.head_object(Bucket=self._link, Key=path)["ContentLength"]

    @StorageEngine.assert_file_or_directory
    def stat(self, path: str) -> os.stat_result:
        if path == "":
            return os.stat_result((-1, -1, -1, -1, -1, -1, -1, -1, -1, -1))
        if self.is_dir(path):
            path = self._normalize_directory_path(path)
        st_mtime = self._aws.head_object(Bucket=self._link, Key=path)["LastModified"].timetuple()
        st_uid, *_ = [
            record.get("Owner", {"ID": "-1"})["ID"]
            for record in self._aws.list_objects_v2(Bucket=self._link, Prefix=path)["Contents"]
            if record["Key"] == path
        ]
        return os.stat_result((-1, -1, -1, -1, int(st_uid), -1, -1, -1, int(time.mktime(st_mtime)), -1))

    def exists(self, path: str) -> bool:
        return self.is_file(path) or self.is_dir(path)

    def is_file(self, filepath: str) -> bool:
        if filepath.endswith("/") or filepath == "":
            return False
        try:
            self._aws.head_object(Bucket=self._link, Key=filepath)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            # something else went wrong:
            raise
        return True

    def is_dir(self, dirpath: str) -> bool:
        if dirpath == "":
            return True
        dirpath = self._normalize_directory_path(dirpath)
        try:
            return self._aws.head_object(Bucket=self._link, Key=dirpath)["ContentLength"] == 0
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            # something else went wrong:
            raise

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
        self._aws.put_object(Bucket=self._link, Body="", Key=dir_name)

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
        response = self._aws.list_objects_v2(Bucket=self._link, Prefix=dirpath).get("Contents", [])
        result = []
        for item in response:
            if len(item["Key"]) > pref_len:
                item = item["Key"][pref_len:].split("/", 1)[0]
                if item not in result and item != "":
                    result.append(item)
        return result

    @StorageEngine.assert_file
    def get_hashsum(self, remote_path: str, hash_type: Enum = StorageEngine.Hash.MD5) -> bytes:
        return self._aws.head_object(Bucket=self._link, Key=remote_path)["ETag"][1:-1]

    def _upload_file(self, remote_path: str, local_path: str, *args, **kwargs) -> None:
        self.optional_file_path_check(remote_path)
        self._aws.upload_file(local_path, self._link, remote_path)

    @StorageEngine.assert_file
    def _download_file(self, remote_path: str, local_path: str, *args, **kwargs) -> None:
        self.optional_file_path_check(remote_path)
        self._aws.download_file(self._link, remote_path, local_path)
