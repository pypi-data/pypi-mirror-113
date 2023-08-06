# Documentation for bacx storage
Last update: 14.07.2021

* [Storage manager](#Storage-manager)
  * [Quick example](#Quick-example)
  * [Storage manager methods](#Storage-manager-methods)
  * [Configuration options](#Configuration-options)
* [Local storage engine](#Local-storage-engine)
* [Aws storage engine](#Aws-storage-engine)
* [Google cloud storage engine](#Google-cloud-storage-engine)
* [Custom storage engine](#Custom-storage-engine) 
* [Example of some file operations](#Example-of-some-file-operations)

## Storage manager:

Storage manager integrates multiple storage engines to one place. Storage manager takes configuration file
(yaml or python dictionary) and set-ups storage engines according to configuration. 

### Quick example:

Configuration file:
```yaml
version: 1
settings:
  cache: null
storages:
  my_local_files:
    type: local
    link: /path/to/folder
```
And create storage manager:
```python
from bacx.storage.manager import StorageManager
stor_man = StorageManager(path="configuration.yml")
stor_man['my_local_files'].open("yourFilename")
```
If you have configuration in dictionary, you can use it instead of configuration file:
```python
stor_man = StorageManager(config=dict_with_configuration)
```

### Storage manager methods:

### `default_storage()`
returns default storage engine. Storage engine can be set to be default by `is_default: True`.

### `storages()`
returns iterator over storage engines.

### `storage_names()`
returns list of names of storage engines. 

You can also check, if storage name `name` is in Storage manager using:
```python
"name" in stor_man
```

### Configuration options:

#### Structure:
```yaml
version: 1
settings:
  ...
storages:
  ...
```

#### Version:
```yaml
version: 1
```
currently only version `1` is supported.

#### Settings:
* Cache settings:
  ```yaml
  # Do not use cache. 
  # If engine requires cache (e.g. cloud engine) an exception will be raised.
  cache: null
  ```
  ```yaml
  # Use default OS cache folder.
  # Cache won't be cleared after code finishes.
  cache: default
  ```
  To specify cache clean option and cache location, use nested configuration:
  ```yaml
  cache:
    path: default or /absolute/cache/path
    on_shutdown: clean or null
  ```

#### Storages:

Storage engine's dictionary consists from pairs `name_of_storage_engine: configuration`. Example:
```yaml
storages:
  my_drive_1:
    ...
  my_drive_2:
    ...
  my_backup_drive:
    ...
  remote_files:
    ...
  ...
```
Each storage configuration consists at least from pairs:
```yaml
type: local or aws or gcloud or custom
is_default: True or False, default is False
link: mounting point
other: optional dictionary
```
To see these settings explained in details, look at specific storage engine.

To learn more, see documentation:
```python
from bacx.storage.manager import StorageManager
help(StorageManager)
```

## Local storage engine
Local storage engine resides on physical drive. Example of configuration may look like:
```yaml
version: 1
settings:
  cache: default
storages:
  my_local_files:
    type: local
    link: /path/to/folder
    is_default: True or False, default is False
    other: is ignored    
```

To learn more, see documentation:
```python
from bacx.storage.engines.local_drive import LocalDrive
help(LocalDrive)
```

## Aws storage engine:
Aws storage engine is connector to Amazon's boto3 S3 storage. Example of configuration may look like:
```yaml
version: 1
settings:
  cache: default
storages:
  my_aws:
    type: aws
    link: bucket-name
    is_default: True or False, default is False
```
Key `other` may contain credentials. Otherwise, credentials will be searched by Amazon's `boto3` library itself.
```yaml
other:
  key_id: 'af654654654ds65...'
  key: 'd2g5465v46546546...'
```

To learn more, see documentation in code. For example:
```python
from bacx.storage.engines.aws_drive import AwsDrive
help(AwsDrive)
```

### Some important aws notes:
* Aws boto3 s3 storage is flat. That means, `StorageEngine` has to simulate directories. It also means, that if 
  content on remote was not created by `AwsDrive` operations, some content may be not accessible in some cases. 
  For example, there can be file `file` and also `file/` on remote, but `AwsDrive` won't allow to interpret `file/` as
  file, because it has `/` at the end (and this is reserved for names for directories). 
  To see more, read `help(AwsDrive)`
* listing directory with filter and depth may be very slow (requires too many requests to remote)


## Google cloud storage engine:
TODO

## Custom storage engine:

Custom storage engine allows you to use your own implementation of your storage engine. 
First of all, you have to implement new `StorageEngine` (or `CloudStorageEngine`). To do that,
see documentation for both of these classes. Then you can load your own python script with this implementation to 
Storage manager using `type: custom` and `module:` options:
```yaml
version: 1
settings:
  cache: default
storages:
  my_local_files:
    type: custom
    link: /path/if/you/need/it
    module: package.path.to.your.script.YourEngineClassName
```

## Example of some file operations

To see how `StorageEngine` file operations works, you can play with this example script. This script is also useful
if you implement new `StorageEngine`, and you want to test, if your implementation works as expected.
The easiest way is to use a `LocalStorage`'s configuration. Place this configuration to `config.yaml`:
```yaml
version: 1
settings:
  cache: null
storages:
  drive:
    type: local
    link: /folder/where/file/operations/will/be/performed
```
Then try this code:<br>
**Note:** this code was tested with `AwsDrive`. If you will be running it with `LocalDrive` some exceptions may look
different (this issue is related to one task). 
```python
from bacx.storage.manager import StorageManager
from bacx.storage.engines.engine import StorageEngine
stor_man = StorageManager("configuration.yml")

# CREATE DIRECTORY AND LIST:
stor_man['drive'].mkdirs("batches/2021-06")
stor_man['drive'].mkdir("test")
stor_man['drive'].list("")
# ['batches', 'test']
stor_man['drive'].list("", filter=StorageEngine.Filter.DIR, depth=2)
# ['batches', 'batches/2021-06', 'test']
stor_man['drive'].list("batches", filter=StorageEngine.Filter.DIR_AND_FILE, depth=2)
# ['2021-06']
stor_man['drive'].mkdir("dir")
stor_man['drive'].list("", filter=StorageEngine.Filter.DIR)
# ['batches', 'dir', 'test']
stor_man['drive'].mkdir("dir")
# Traceback (most recent call last):
# ...
# IsADirectoryError: Directory `dir/` already exists.
stor_man['drive'].exists("dir")
# True
stor_man['drive'].is_dir("dir")
# True
stor_man['drive'].stat("dir")
# os.stat_result(st_mode=-1, st_ino=-1, st_dev=-1, st_nlink=-1, st_uid=-1, st_gid=-1, st_size=-1, st_atime=-1, st_mtime=1626275955, st_ctime=-1)
stor_man['drive'].size("dir")
# 0
stor_man['drive'].size("")
# 0


# CREATE SUB FILE AND TRY TO REMOVE SUPER DIR:
stor_man['drive'].mkfile("dir/file")
stor_man['drive'].delete("dir")
# Traceback (most recent call last):
# ...
# FileNotFoundError: File `dir` does not exists.
stor_man['drive'].rmdir("dir")
# Traceback (most recent call last):
# ...
# OSError: Directory `dir` is not empty.
stor_man['drive'].rmtree("dir")
stor_man['drive'].exists("dir/file")
# False
stor_man['drive'].exists("dir")
# False


# CREATE FILE-DIR CONFLICT:
stor_man['drive'].mkfile("problem")
stor_man['drive'].mkdir("problem")
# Traceback (most recent call last):
# ...
# FileExistsError: File `problem` already exists.
stor_man['drive'].delete("problem")
stor_man['drive'].mkdir("problem")
stor_man['drive'].mkfile("problem")
# Traceback (most recent call last):
# ...
# IsADirectoryError: Path `problem` is a directory.
stor_man['drive'].rmdir("problem")


# MAKE MORE DIRECTORIES AT ONCE:
stor_man['drive'].mkdirs("ndir/sub")


# READ AND WRITE TO NEW FILE:
stor_man['drive'].write_as_text("ndir/sub/file", "Awesome file")
# (you can now go to cache and try to change content of cached file)
stor_man['drive'].read_as_text("ndir/sub/file")
# 'Awesome file'
stor_man['drive'].mkdirs("ndir/sub/file/bad_dir")
# Traceback (most recent call last):
# ...
# FileExistsError: File `ndir/sub/file` already exists.
stor_man['drive'].mkdir("ndir/sub/file/bad_dir")
# Traceback (most recent call last):
# ...
# FileExistsError: File `ndir/sub/file` is a file.
stor_man['drive'].mkdir("ndir/sub/foo/bar")
# Traceback (most recent call last):
# ...
# FileNotFoundError: Path `ndir/sub/foo` is not a directory.
stor_man['drive'].mkdirs("ndir/sub/foo/bar")
stor_man['drive'].list("ndir", depth=7)
# ['sub', 'sub/file', 'sub/foo', 'sub/foo/bar']
stor_man['drive'].list("ndir", filter=StorageEngine.Filter.DIR, depth=7)
# ['sub', 'sub/foo', 'sub/foo/bar']


# SOME FILE OPERATIONS:
with stor_man['drive'].open("ndir/file2", "w") as file:
    file.write("Hello universal drive!")

# 22
stor_man['drive'].read_as_bytes("ndir/file2")
# b'Hello universal drive!'
stor_man['drive'].download_to_file("ndir/file2", "/some/path/file2")
with open("/some/path/file2", "r") as file:
    print(file.read())

# Hello universal drive!
stor_man['drive'].upload_from_file("ndir/sub/foo/file2-copy", "/some/path/file2")
stor_man['drive'].read_as_text("ndir/sub/foo/file2-copy")
# 'Hello universal drive!'
stor_man['drive'].stat("ndir/sub/foo/file2-copy")
# os.stat_result(st_mode=-1, st_ino=-1, st_dev=-1, st_nlink=-1, st_uid=-1, st_gid=-1, st_size=-1, st_atime=-1, st_mtime=1626279047, st_ctime=-1)
stor_man['drive'].size("ndir/sub/foo/file2-copy")
# 22
stor_man['drive'].list("ndir", depth=7)
# ['file2', 'sub', 'sub/file', 'sub/foo', 'sub/foo/bar', 'sub/foo/file2-copy']
stor_man['drive'].list("ndir", filter=StorageEngine.Filter.FILE, depth=7)
# ['file2', 'sub/file', 'sub/foo/file2-copy']
stor_man['drive'].rmtree("ndir")
stor_man['drive'].exists("ndir")
# False
stor_man['drive'].mkfile("dirNotExists/file")
# Traceback (most recent call last):
# ...
# NotADirectoryError: Path `dirNotExists` is not a directory.
stor_man['drive'].mkfile("fileCantEndWithSlash/")
# Traceback (most recent call last):
# ...
# ValueError: File name can't end with `/` symbol.
```
