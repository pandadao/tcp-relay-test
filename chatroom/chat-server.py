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

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_socket = chatlib.socketInit((host, chatlib.port))

lobby = Lobby()
connection_list = []
connection_list.append(listen_socket)

while True:
    r_user, w_user, e_user = select.select(connection_list, [], [])
    for user in r_user:
        if user is listen_socket: #新連線,這邊的user代表socket物件
            new_socket, add = user.accept()
            new_user = User(new_socket)
            connection_list.append(new_user)
            lobby.new_socket_client(new_user)

        else: #新訊息處理
            print("33")
            msg = user.socket.recv(MSG_BUFFER)
            if msg: #如果有接收到訊息進來
                msg = msg.decode('utf-8').lower()
                lobby.handle_msg(user, msg)

            else:
                print ("39")
                user.socket.close()
                connection_list.remove(user)

    for s in e_user: #關閉任何錯誤的socket連線,以確保server有足夠資源處理其他連線請求
        s.close()
        connection_list.remove(s)
