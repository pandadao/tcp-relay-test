# -*- coding:utf-8 -*-

from __future__ import print_function
import socket
import os
import select
from chatlib import Lobby, RoomFunction, User
import chatlib
import sys
import threading
import Queue
from io import BytesIO

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
print("Connecting to server")
msg_prefix = ''

inputs = [connect_to_server]
outputs = []
message_queue = {}

while True:
    r_list, w_list, e_list = select.select(inputs, outputs, inputs)
    for s is connect_to_server:



'''
select module for windows
'''
'''
#socket_list = [sys.stdin, connect_to_server]
stdin_buf = BytesIO()
stdout_buf = BytesIO()
stderr_buf = BytesIO()

r_select = [sys.stdout, sys.stderr]
w_select = [sys.stdin]
read_bytes_size = 4096

input_queue = Queue.Queue(maxsize = -1)
output_queue = Queue.Queue(maxsize = -1)
error_queue = Queue.Queue(maxsize = -1)

no_more_output = threading.Lock()
no_more_output.acquire()
no_more_error = threading.Lock()
no_more_error.acquire()

def put_input(input_queue):
    while True:
        sys.stdout.flush() #不將stdout存進buffer
        b = stdin_buf.read(MSG_BUFFER)
        if b:
            input_queue.put(b)
        else:
            break

def get_output(output_queue):
    while not no_more_output.acquire(False):
        b = os.read(sys.stdout.fileno(), MSG_BUFFER)
        if b:
            output_queue.put(b)

def get_error(error_queue):
    while not no_more_error.acquire(False):
        b = os.read(sys.stderr.fileno(), MSG_BUFFER)
        if b:
            error_queue.put(b)


input_thread = threading.Thread(target = put_input, args = (input_queue,))
input_thread.start()
output_thread = threading.Thread(target = get_output, args = (output_queue,))
output_thread.start()
error_thread = threading.Thread(target = get_error, args = (error_queue,))
error_thread.start()

output_ready = False
error_ready = False

while(len(w_select) + len(r_select)) > 0:
    try:
        if sys.stdin in w_select:
            if not input_queue.empty():
                os.write(sys.stdin.fileno(), input_queue())
            elif not input_thread.is_alive():
                w_select = []
        if sys.stdout in r_select:
            if not output_queue.empty():
                output_ready = True
                stdout_buf.write(output_queue.get())
            elif output_ready:
                r_select = []
                no_more_output.release()
                no_more_error.release()
                output_thread.join()

        if sys.stderr in r_select:
            if not error_queue.empty():
                error_ready = True
                stderr_buf.write(error_queue.get())
            elif error_ready:
                r_select = []
                no_more_output.release()
                no_more_error.release()
                output_thread.join()
                error_thread.join()
        if stdout_buf.getvalue().endswith("\n"):
            r_select = []
            no_more_output.release()
            no_more_error.release()
            output_thread.join()
    except:
        break
'''
