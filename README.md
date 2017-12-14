# CS7NS1 Distributed File System

## Components implemented

- [x] File Service
- [x] Directory Service
- [x] Lock Service
- [x] Client (transparent file access)
- [x] Caching

## Running

I run the distributed file system using a combination of docker, docker-machine and docker-compose.

The `launch.sh` script wil run the following two steps:

**1. Run the services**
```shell
$ docker-compose build
$ docker-compose up -d
```
**2. Create the databases**
```shell
$ docker-compose run lock-service python manage.py recreate_db
$ docker-compose run directory-service python manage.py recreate_db
```

**Run client**
```shell
$ cd client
$ python client.py
```

## File Service

The File Service stores static files on its own file system. It exposes an API that the Directory Service can use to manipulate the files using CRUD operations.

**API**

| HTTP verb | Endpoint | Description |
| --------- | -------- | ------------|
| GET       | /files   | Get list of all files stored on this server |
| GET | /files/:filename | Get file :filename |
| POST | /files | Save the file contained in the request body to this file server. If it already exists, overwrite it |
| DELETE | /files/:filename | Delete :filename from this server |

## Directory Service

**File object**

```python
class File():
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(128), nullable=False)
```

**API**

| HTTP verb | Endpoint | Description |
| --------- | -------- | ------------|
| GET       | /files   | Get list of all files in the dfs (all file servers) |
| GET | /files/:filename | Attemp to get (open) file :filename from whichever file server it is stored on and also place a lock on it for the user. If already locked this will return an error code to the client |
| POST | /files | Upload the file contained in the request body to a random file server, storing it in the Directory Service's database |
| PUT | /files/:filename | Update (close) :filename by writing the new contents to whichever server it is stored on, and release the lock. If already locked this will return an error code to the client. 
| DELETE | /files/:filename | Delete :filename from whichever server it is stored on |

## Lock Service

Keeps a database table of `FileLock` objects (see below). If a FileLock entry exists for a particular file, then it is locked by the user in the `FileLock.user` field. If it is not in the database, then it is assumed to be unlocked.

**FileLock object**
```python
class FileLock():
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    user = db.Column(db.String(128), nullable=False)
```

**API**

| HTTP verb | Endpoint | Description |
| --------- | -------- | ------------|
| GET       | /locks   | List of all FileLocks held by this ervice |
| GET | /locks/:id | Get the lock corresponding to file with id of :id (if it exists) |
| POST | /locks | Lock a file by storing a FileLock in the db corresponding to a file |
| DELETE | /locks/:id | Unlock file with id of :id, deleting lock from db |