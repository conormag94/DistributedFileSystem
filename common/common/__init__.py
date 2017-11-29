import hashlib

import requests

FILE_SERVER_HOST = '192.168.99.100'
FILE_SERVER_PORT = 5001

FILE_SERVER = f'http://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}/files'

def list_files():
    response = requests.get(FILE_SERVER).json()
    file_list = response['data']['files']
    return file_list

def get_file(filename):
    url = f'{FILE_SERVER}/{filename}'
    file_obj = requests.get(url).json()
    return file_obj['data']

def create_file(filename, content):
    json_body = {
        "filename": filename,
        "content": content
    }
    response = requests.post(FILE_SERVER, json=json_body).json()
    return response

def compute_hash(data):
    """
    Return the hash of a file's contents
    """
    hash_obj = hashlib.md5()
    hash_obj.update(data.strip())
    return hash_obj.hexdigest()