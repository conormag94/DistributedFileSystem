import os
import requests
import sys


prompt = '\033[1;33m' + '> ' + '\033[0;0m'

FILE_SERVER_HOST = sys.argv[1]
FILE_SERVER_PORT = 5001

FILE_SERVER = f'http://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}/files'

def list_files():
    response = requests.get(FILE_SERVER).json()
    file_list = response['data']['files']
    for file in file_list:
        print(file['filename'], '\t', file['created_at'])

def main():
    while(True):
        cmd = input(prompt)
        if cmd == 'q':
            sys.exit(1)
        if cmd == 'list':
            list_files()
        else:
            print(cmd)

def greeting():
    print('===== Distributed File System Client =====')

if __name__ == '__main__':
    greeting()
    main()