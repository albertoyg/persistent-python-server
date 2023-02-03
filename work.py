#!/usr/bin/env python3

import select
import socket
import sys
import queue
import time
import re

f = open("multiple_requests_1.txt", "r")
entireMessage = f.read()
splitEm = entireMessage.split('\n\n')
# print(splitEm)
                
#                 # First check if bad requests
requestLine = []


f1 = re.compile(r"GET /.+ HTTP/1.0")
f2 = re.compile(r"GET /.+ HTTP/1.0\nConnection:Keep-alive")
f3 = re.compile(r"GET /.+ HTTP/1.0\nConnection: keep-alive")


for message in splitEm:
    if not re.search(f1, message) and not re.search(f2, message) and not re.search(f3, message):
        print(message)
        # cut connection



# if not match:
#     bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
#     message_queues[connection].put(bad_request)
          
                    
# else:
#     print("Match found!")