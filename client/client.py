import os
import sys


import requests


prompt = '\033[1;32m' + '> ' + '\033[0;0m'

CACHE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cached_files')

DIRECTORY_SERVICE = "http://192.168.99.100:5000"

def list_files():
    """
    Get list of all files from the directory service.
    """
    url = f"{DIRECTORY_SERVICE}/files"
    r = requests.get(url).json()
    return r

def get_file(filename):
    """
    Get a file from the directory service.
    """
    url = f"{DIRECTORY_SERVICE}/files/{filename}"
    r = requests.get(url)
    return r

def read_file(filename):
    """
    Print the contents of a locally cached file.
    """
    cached_file = os.path.join(CACHE_LOCATION, filename)
    if not os.path.exists(cached_file):
        print(f"{filename} not cached locally")
        print(f"You may need to open it first with the \'open\' command")
    else:
        filesize = os.stat(cached_file).st_size
        with open(cached_file, 'rb') as f:
            print('\033[1;35m', end="")
            print(f"  {filename}:")
            print('\033[0;0m', end="")
            print(f.read().decode())

def greeting():
    print('Commands:')
    print('---------')
    print('  ls            - List files (remote and cached)')
    print('  open <file>   - Download file from remote file system')
    print('  read <file>   - Read contents of locally cached file (.txt files only)')
    print('  upload <file> - Upload a file to the DFS')
    print('  help          - Show this menu again')
    print('  q             - Quit')
    print('---------')

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
        elif cmd[0] == 'read':
            filename = cmd[1]
            read_file(filename)
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
        elif cmd[0] == 'help':
            greeting()
        else:
            print("Error: Unrecognized command")
            greeting()

if __name__ == '__main__':
    greeting()
    main()