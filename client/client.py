import os
import requests
import sys


def greeting():
    print('===== Distributed File System Client =====')

def main():
    while(True):
        inp = input('> ')
        if inp == 'quit':
            sys.exit(1)
        else:
            print(inp)

if __name__ == '__main__':
    greeting()
    main()