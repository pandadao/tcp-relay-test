# -*- coding: utf-8 -*-
'''
import select
import socket
import Queue
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

server_address = ('127.0.0.1', 8090)
print ("starting up on %s port %s" % server_address)
server.bind(server_address)

server.listen(5)

inputs = [server]

outputs = []
message_queue = {}

while inputs:
    print ('waiting for next event')
    readable, writeable, excep = select.select(inputs, outputs, inputs)

    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print ('client connection from ', client_address)
            connection.setblocking(0)
            inputs.append(connection)

            message_queue[connection] = Queue.Queue()

        else:
            data = s.recv(1024)
            if data != '':
                print ('received %s from %s' % (data, s.getpeername()))
                message_queue[s].put(data)
                if s not in outputs:
                    outputs.append(s)

            else:
                print ('client closing', client_address)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                del message_queue[s]

    for s in writeable:
        try:
            message_queue = message_queue.get(s)
            send_data = ''
            if message_queue is not None:
                send_data = message_queue.get_nowait()
            else:
                print ("client has closed")
        except Queue.Empty:
            print("%s" % (s.getpeername()))
            outputs.remove(s)

        else:
            if message_queue is not None:
                s.send(send_data)
            else:
                print ("client has closed")

    for s in excep:
        print("exception condition on ", s.getpeername())
        inputs.remove(s)

        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queue[s]
    sleep(1)
'''
# -*- coding: utf-8 -*-
import socket,select
connection_list = []
host = ''
port = 10001
def board_cast(sock,message):
    for socket in connection_list:
        if socket != server_sock and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
            print (str(socket.getpeername()) ,' is offline')
            connection_list.remove(socket)

server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_sock.setblocking(0)
server_sock.bind((host,port))
server_sock.listen(10)
connection_list.append(server_sock)
while 1:
    readable,writable,error = select.select(connection_list,[],[])
    for sock in readable:
        if sock == server_sock:
            connection,connection_add = sock.accept()
            message = str(connection_add) + 'enter room'
            board_cast(connection,message)
            print connection_add,'%s connect'
            connection_list.append(connection)
        else:
            try:
                date = sock.recv(1024)
                print date
                board_cast(sock,'(' + str(sock.getpeername())  +') :' + date)
            except:
                message2 = str(sock.getpeername()) + 'is offline'
                board_cast(sock,message2)
                print str(sock.getpeername()) + ' is offline'
                sock.close()
                connection_list.remove(sock)
                continue
