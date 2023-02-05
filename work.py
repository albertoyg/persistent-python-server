#!/usr/bin/env python3

import select
import socket
import sys
import queue
import time
import re
import os

#  NEED TO TRY OUT NGINGX TO SEE HOW IT ACTS THEN U GOOD 


def checkForFile(requestline):
    decode = requestline.split()
    filename = decode[1][1:]
    return (os.path.isfile(filename), filename)

f = open("multiple_requests_1.txt", "r")
entireMessage = f.read()
messages = entireMessage.split('\n')

for curRequest in range(len(messages)):
    # check if request is in correct GET.... format
    if re.search(re.compile(r"GET /.* HTTP/1.0"), messages[curRequest]):
        # if it is, check if next request is connection: alive
        if re.search(re.compile(r"connection:\s*Keep-alive", re.IGNORECASE), messages[curRequest+1]):
            # if connection: keep-alive, check if file exists 
            found, filename = checkForFile(messages[curRequest])
            if found: 
                ok = 'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\n\r\n'
                #   PRINT OK MESSAGE TO CLIENT 
                #   message_queues[connection].put(ok)
                #   BUT FOR NOW....
                print(ok)
                # output file contents 
                HTMLfile = open(filename, 'r')
                #   PRINT file contents TO CLIENT 
                #   message_queues[connection].put(HTMLfile.read())
                #   BUT for now....
                print(HTMLfile.read())

            else:
        #       # file not found
                not_found = 'HTTP/1.0 404 Not Found\r\nConnection: keep-alive\r\n\r\n'
                #   PRINT notfound MESSAGE TO CLIENT 
                #   message_queues[connection].put(nout_found)
                #   BUT FOR NOW....
                print(not_found)
        else:
            # check for bad header line
            if not re.search(re.compile(r"connection:\s*close", re.IGNORECASE), messages[curRequest+1]) and messages[curRequest + 1] != '':
                # if we are here, the header line is bad
                bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
                #   PRINT notfound MESSAGE TO CLIENT 
                #   message_queues[connection].put(bad_request)
                #   BUT FOR NOW....
                print(bad_request, 'CLOSING NOW BECASUE BAD')
        # if connection: closed, check if file exists 
            found, filename = checkForFile(messages[curRequest])
            if found: 
                ok = 'HTTP/1.0 200 OK\r\n\r\n'
                #   PRINT OK MESSAGE TO CLIENT 
                #   message_queues[connection].put(ok)
                #   BUT FOR NOW....
                print(ok)
                # output file contents 
                HTMLfile = open(filename, 'r')
                #   PRINT file contents TO CLIENT 
                #   message_queues[connection].put(HTMLfile.read())
                #   BUT for now....
                print(HTMLfile.read())

                # CLOSE CONNECTION
                print('CLOSING CONNECTION HERE\r\n')
            else:
        #       # file not found
                not_found = 'HTTP/1.0 404 Not Found\r\nConnection: close\r\n\r\n'
                #   PRINT notfound MESSAGE TO CLIENT 
                #   message_queues[connection].put(not_found)
                #   BUT FOR NOW....
                print(not_found)
            
                # CLOSE CONNECTION
                print('CLOSING CONNECTION HERE\r\n')

    # check if end of requests: \n\n
    elif messages[curRequest] == '':
        # empty line detected
        if curRequest + 1 < len(messages):
            # check if it's last line
            if messages[curRequest + 1] == '':
                # if we are here, last two lines are empty
                print('end of file, closing connectoion. Thank you. ')

    # BAD REQUEST  
    else:
        # ensure it's not the header
        if not re.search(re.compile(r"connection:\s*Keep-alive", re.IGNORECASE), messages[curRequest]) and not re.search(re.compile(r"connection:\s*close", re.IGNORECASE), messages[curRequest]) and messages[curRequest] != '':
            bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
            #   PRINT notfound MESSAGE TO CLIENT 
            #   message_queues[connection].put(bad_request)
            #   BUT FOR NOW....
            print(bad_request)