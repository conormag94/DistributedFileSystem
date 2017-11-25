import hashlib

import requests

FILE_SERVER_HOST = '192.168.99.100'
FILE_SERVER_PORT = 5001

FILE_SERVER = f'http://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}/files'

def list_files():
    response = requests.get(FILE_SERVER).json()
    file_list = response['data']['files']
    return file_list

def compute_hash(data):
    """
    Return the hash of a file's contents
    """
    hash_obj = hashlib.md5()
    hash_obj.update(data.strip())
    return hash_obj.hexdigest()