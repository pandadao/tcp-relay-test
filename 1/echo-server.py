# -*- coding:utf-8 -*-
#Author: pandadao

import sys
import socket

def usage():
    print "Usage: ./echoserver [relay IP] [relay port]"
    sys.exit(1)


if __name__ == '__main__':
    host = ''
    port = ''
    size = 4096

    # Check the command is correct or not
    total = len(sys.argv)
    if total < 3:
        usage()

    host = sys.argv[1]
    port = int(sys.argv[2])

    if not (host or port):
        usage()

    # Connect to the relay server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Receive a host & port information
    recieve_data = s.recv(size)
    print recieve_data

    # Receiveing data flow
    running = 1
    while running:
        data = s.recv(size)
        if data:
            s.send(data)
        else:
            running = 0

    s.close()
