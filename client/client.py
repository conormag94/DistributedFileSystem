import os
import sys


import requests


current_user = 'NO_USER'

CACHE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cached_files')

DIRECTORY_SERVICE = "http://192.168.99.100:5000"

def prompt(username):
    return '\033[1;32m' + username + ': ' + '\033[0;0m'

def switch_user(new_user):
    global current_user
    current_user = new_user
    print(f"Now logged in as {new_user}")

def is_cached(filename):
    cached_file = os.path.join(CACHE_LOCATION, filename)
    return os.path.exists(cached_file)

def cache_path(filename):
    return os.path.join(CACHE_LOCATION, filename)

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
    headers = {'user': current_user}
    r = requests.get(url, headers=headers)
    return r

def read_file(filename):
    """
    Print the contents of a locally cached file.
    """
    if not is_cached(filename):
        print(f"{filename} not cached locally")
        print(f"You may need to open it first with the \'open\' command")
    else:
        cached_file = os.path.join(CACHE_LOCATION, filename)
        filesize = os.stat(cached_file).st_size
        with open(cached_file, 'rb') as f:
            print('\033[1;35m', end="")
            print(f"  {filename}:")
            print('\033[0;0m', end="")
            print(f.read().decode())

def greeting():
    print('Commands:')
    print('---------')
    print('  ls                   - List files (remote and cached)')
    print('  login <user>         - Login as <user> instead of the default user')
    print('  open <file>          - Download file from remote file system')
    print('  close <file>         - Send any local reads/writes back to remote file system')
    print('  read <file>          - Read contents of locally cached file (.txt files only)')
    print('  write <file> <data>  - Write <data> to locally cached file (.txt files only)')
    print('  upload <file>        - Upload a file to the DFS')
    print('  help                 - Show this menu again')
    print('  q                    - Quit')
    print('---------')

def main():
    while(True):
        p = prompt(current_user)
        cmd = input(p).split(' ')
        if len(cmd) > 1:
            filename = cmd[1]
        
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
        elif cmd[0] == 'login':
            username = cmd[1]
            switch_user(username)
        elif cmd[0] == 'open':
            response = get_file(filename)
            if response.status_code == 200:
                save_path = os.path.join(CACHE_LOCATION, filename)
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                    print(f"\'{filename}\' saved to {save_path}")
            else:
                error_msg = response.json()["message"]
                print(f"\'{filename}\': {error_msg}")
        elif cmd[0] == 'close':
            if not is_cached(filename):
                print(f"{filename} not cached locally")
                print(f"You may need to open it first with the \'open\' command")
            else:
                filepath = cache_path(filename)
                with open(filepath, 'rb') as f:
                    url = f"{DIRECTORY_SERVICE}/files/{filename}"
                    r = requests.put(url, files={'user_file': (filename, f)})
                    print(r.status_code, "-", r.content.decode())
        elif cmd[0] == 'read':
            read_file(filename)
        elif cmd[0] == 'write':
            if not is_cached(filename):
                print(f"{filename} not cached locally")
                print(f"You may need to open it first with the \'open\' command")
            else:
                data = " ".join(cmd[2:])
                cached_file = os.path.join(CACHE_LOCATION, filename)
                with open(cached_file, 'wb') as f:
                    f.write(data.encode())
                    print("Written sucessfully")
            
        elif cmd[0] == 'upload':
            filepath = os.path.expanduser(cmd[1])
            filename = os.path.basename(filepath)
            if not os.path.exists(filepath):
                print(f"{filename} not found on this file system")
            else:
                with open(filepath, 'rb') as f:
                    url = f"{DIRECTORY_SERVICE}/files"
                    r = requests.post(url, files={"user_file": (filename, f)})
                    print(r.status_code, "-", r.content.decode())
        elif cmd[0] == 'help':
            greeting()
        else:
            print("Error: Unrecognized command")
            greeting()

if __name__ == '__main__':
    greeting()
    switch_user('user')
    main()