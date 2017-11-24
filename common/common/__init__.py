import requests

FILE_SERVER_HOST = '192.168.99.100'
FILE_SERVER_PORT = 5001

FILE_SERVER = f'http://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}/files'

def list_files():
    response = requests.get(FILE_SERVER).json()
    file_list = response['data']['files']
    for file in file_list:
        print(file['filename'], '\t', file['created_at'])