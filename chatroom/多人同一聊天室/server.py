# -*- coding:utf-8 -*-
import socket
import select
import thread


port = 5963
server_addr = ("0.0.0.0", port)

# 紀錄socket連線物件,用來回應聊天室
inputs = []

#init socket
def serverInit(self):
    s_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_s.bind(server_addr)
    s_s.listen(10)
    return s_s

# python取得host沒在使用的port number
'''
def fp():
    s = socket.socket()
    s.bind(("",0))
    addr, port = s.getsockname()
    return addr, port

while True:
    try:
        addr1, port1 = fp()
        print port1
    except KeyboardInterrupt:
        break
'''
