# -*- coding:utf8 -*-

from __future__ import print_function
import socket
import os
import select
from chatlib import Lobby, RoomFunction, User
import chatlib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

MSG_BUFFER = 4096

if len(sys.argv) < 2:
    print ("請輸入 python chat-client.py [server_addr]", file = sys.stderr)
    sys.exit(1)

else:
    connect_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect_to_server.connect((sys.argv[1], chatlib.port))

def prompt():
    print('>', end= ' ', file = sys.stdout.flush())

print("正在連接server\n")
msg_prefix = ''

socket_list = [sys.stdin, connect_to_server]
while True:
    r_list, w_list, e_list = select.select(socket_list, [], [])
    for s in r_list:
        if s is connect_to_server: #連入的socket
            msg = s.recv(MSG_BUFFER)
            if not msg:
                print ("服務中斷")

            else:
                if msg == chatlib.QUIT_COMMAND.encode('utf-8'):
                    sys.stdout.write('Bye\n')
                    sys.exit(2)

                else:
                    sys.stdout.write(msg.decode('utf-8'))
                    if 'Please keyin your name' in msg.decode('utf-8'):
                        msg_prefix = 'name: ' #辨識名字

                    else:
                        msg_prefix = ''
                    prompt()

        else:
            msg = msg_prefix + sys.stdin.readline()
            connect_to_server.sendall(msg.encode('utf-8'))
