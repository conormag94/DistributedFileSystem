import os
import sys


import requests


prompt = '\033[1;32m' + '> ' + '\033[0;0m'

CACHE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cached_files')

DIRECTORY_SERVICE = "http://192.168.99.100:5000"

def list_files():
    url = f"{DIRECTORY_SERVICE}/files"
    r = requests.get(url).json()
    return r

def get_file(filename):
    url = f"{DIRECTORY_SERVICE}/files/{filename}"
    r = requests.get(url)
    return r

def greeting():
    print('Commands:')
    print('---------')
    print('ls\tList files')
    print('open <filename>\tDownload file from remote file system')
    print('upload <filepath>\tUpload a file to the DFS')
    print('q\tQuit')

def main():
    while(True):
        cmd = input(prompt).split(' ')
        
        if cmd[0] == 'q':
            sys.exit(1)
        
        elif cmd[0] == 'ls':
            cached_files = os.listdir(CACHE_LOCATION)
            print(f"{len(cached_files)} cached file(s)")
            print("------------------")

            for file in cached_files:
                print(file)

            files = list_files()["files"]
            print(f'\n{len(files)} remote file(s):')
            print("------------------")
            for file in files:
                print(file["filename"])
        
        elif cmd[0] == 'open':
            filename = cmd[1]
            response = get_file(filename)
            if response.status_code == 200:
                save_path = os.path.join(CACHE_LOCATION, filename)
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                    print(f"\'{filename}\' saved to {save_path}")
            else:
                error_msg = response.json()["message"]
                print(f"\'{filename}\': {error_msg}")
        
        elif cmd[0] == 'upload':
            filepath = os.path.expanduser(cmd[1])
            filename = os.path.basename(filepath)
            if not os.path.exists(filepath):
                print(f"{filename} not found on this file system")
            else:
                with open(filepath, 'rb') as f:
                    url = f"{DIRECTORY_SERVICE}/files"
                    r = requests.post(url, files={"user_file": (filename, f)})
                    print(r.status_code, "-", r.content)
            print("Upload not yet implemented")
        
        else:
            print("Error: Unrecognized command")
            greeting()

if __name__ == '__main__':
    greeting()
    main()