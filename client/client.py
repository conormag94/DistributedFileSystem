import os
import sys


import requests


prompt = '\033[1;32m' + '> ' + '\033[0;0m'

CACHE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cached_files')
FILE_SERVER_HOST = 'http://192.168.99.100'

FILE_SERVER_URLS = {
    "1": f"{FILE_SERVER_HOST}:5001/files",
    "2": f"{FILE_SERVER_HOST}:5002/files"
}

def list_files(file_server):
    url = FILE_SERVER_URLS[file_server]
    r = requests.get(url).json()
    return r['files']

def get_file(filename, file_server):
    url = FILE_SERVER_URLS[file_server] + '/' + filename
    r = requests.get(url)
    return r

def greeting():
    print('Commands:')
    print('---------')
    print('ls\tList files')
    print('q\tQuit')

def main():
    while(True):
        cmd = input(prompt).split(' ')
        
        if cmd[0] == 'q':
            sys.exit(1)
        
        elif cmd[0] == 'ls':
            files = list_files(file_server="1")
            print(f'{len(files)} file(s) found:')
            print("------------------")
            for file in files:
                print(file)
        
        elif cmd[0] == 'get':
            filename = cmd[1]
            response = get_file(filename, file_server="1")

            save_path = os.path.join(CACHE_LOCATION, filename)
            with open(save_path, 'wb') as f:
                f.write(response.content)
        
        else:
            print("Error: Unrecognized command")
            greeting()

if __name__ == '__main__':
    greeting()
    main()