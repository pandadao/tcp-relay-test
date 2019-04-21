# -*- coding:utf-8 -*-

from __future__ import print_function
import sys
import threading
import Queue


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
        b = stdin
