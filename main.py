import argparse
import os
from textwrap import dedent

from scanner import PortScanner


MESSAGE = '''
    \033[38;5;196;4mSingle IP or File is required!\033[0m

    usage: main.py [-h] [-ip IP] [-f FILE]

    Simple port scanner using threading.

    options:
    -h, --help            show this help message and exit
    -ip IP                IP address to scan
    -f FILE, --file FILE  Text file containing a list of IPs to scan (one IP per line)
'''

def parse_arguments():
    parser = argparse.ArgumentParser(description='Simple port scanner using threading.')
    parser.add_argument('-ip', help='IP address to scan')
    parser.add_argument('-f', '--file', help='Text file containing a list of IPs to scan (one IP per line)')
    return parser.parse_args()

def open_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    args = parse_arguments()
    if not args.ip and not args.file:
        print(dedent(MESSAGE))
        return

    ip_list = open_file(args.file) if args.file else [args.ip]
    PortScanner(ip_list)

if __name__ == '__main__':
    main()
