# Common library for the DFS

A library of helper functions and classes to be used by the various services in the Distributed File System.

## Installation

Include in the component's `requirements.txt` file like so:
```
-e git://github.com/conormag94/DistributedFileSystem.git#egg=common&subdirectory=common
```
This will install it with pip directly from this github repo

## Usage

Example:
```python 3
from common import list_files

files_list = list_files()
print(files_list) 
```