import os
import sys

from common import list_files


prompt = '\033[1;33m' + '> ' + '\033[0;0m'


def main():
    while(True):
        cmd = input(prompt)
        if cmd == 'q':
            sys.exit(1)
        if cmd == 'list':
            files = list_files()
            for file in files:
                print(file['filename'], '\t', file['created_at'])
        else:
            print(cmd)

def greeting():
    print('     DFS:')
    print('=============')
    print('list\tList files')
    print('q\tQuit')

if __name__ == '__main__':
    greeting()
    main()