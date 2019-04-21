# coding: utf-8

'''
import socket


messages = ['This is the message ', 'It will be sent ', 'in parts ', ]

server_address = ('localhost', 8090)

# Create aTCP/IP socket

socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET,  socket.SOCK_STREAM), ]

# Connect thesocket to the port where the server is listening

print ('connecting to %s port %s' % server_address)
# 连接到服务器
for s in socks:
    s.connect(server_address)

for index, message in enumerate(messages):
    # Send messages on both sockets
    for s in socks:
        print ('%s: sending "%s"' % (s.getsockname(), message + str(index)))
        s.send(bytes(message + str(index)).decode('utf-8'))
    # Read responses on both sockets

for s in socks:
    data = s.recv(1024)
    print ('%s: received "%s"' % (s.getsockname(), data))
    if data != "":
        print ('closingsocket', s.getsockname())
        s.close()
'''

import socket,threading,time
flag = 0
date = ''
lock = threading.Lock()
host = 'localhost'
port = 10001
client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.setblocking(0)
class Mythread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global flag, date
        while 1:
            date = raw_input()
            if len(date):
                lock.acquire()
                flag = 1
                lock.release()
class Mythread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global flag
        global date
        while 1:
            try:
                buf = client_sock.recv(1024)
                if len(buf):
                    print buf
            except:
                pass
            if flag:
                try:
                    client_sock.send(date)
                except socket.error, e:
                    print e
                lock.acquire()
                flag = 0
                lock.release()
try:
    client_sock.connect((host,port))
    print"連線成功"
except socket.error,e:
    print e
t1 = Mythread1()
t2 = Mythread2()
t1.start()
t2.start()
