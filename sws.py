#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2029 Zhiming Huang
#


import select
import socket
import sys
import queue
import time
import re


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
serverPort = int(sys.argv[2])
# Bind the socket to the port
server_address = ('', serverPort)
#print('starting up on {} port {}'.format(*server_address),
#      file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

# request message
request_message = {}

timeout = 30

while inputs:

    # Wait for at least one of the sockets to be
    # ready for processing
#    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs,
                                                    timeout)

    # Handle inputs
    for s in readable:

        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            request_message[connection] = ""
            #new_request[s] = True
            #persistent_socket[connection] = True
            # Give the connection a queue for data
            # we want to send
            message_queues[connection] = queue.Queue()

        else:
            message1 =  s.recv(1024).decode()
            if message1:
                # First check if bad requests

                
#                 patterns = []
                requestLine1 = re.compile(r"GET /.+ HTTP/1.0")
                match = re.search(requestLine1, message1)
                if match:
                    print("Match found!")
                else:
                    print("No match found.")
                    bad_request = 'HTTP/1.0 400 Bad Request\n\n'
                    # message_queues.put(bad_request)
                    request_message[s] = bad_request
                
#                 re.compile('test', re.IGNORECASE)
#                 two = re.compile(r"GET /.+ HTTP/1.0\r\n(?i)Connection:Keep-Alive\r\n\r\n")
#                 patterns.append(two)
#                 five = re.compile(r"GET /.+ HTTP/1.0\r\n\r\n")
#                 patterns.append(five)
#                 six = re.compile(r"GET /.+ HTTP/1.0\r\n(?i)Connection: Closed\r\n\r\n")
#                 patterns.append(six)
#                 seven = re.compile(r"GET /.+ HTTP/1.0\r\n(?i)Connection:Closed\r\n\r\n")
#                 patterns.append(seven)

                
                accepted = False
                
                # check if request matches any format above
#                 for pattern in patterns:
#                     if pattern.match(message1):
#                         accepted = True

                #  if it isn't, return bad request message 
                if accepted == False:
                    bad_request = 'HTTP/1.0 400 Bad Request\n\n'
                    # message_queues.put(bad_request)
                    request_message[s] = bad_request

                # If the request is okay:
                else:

                # check if the end of the requests:
                    if  message[-2:] != '\n\n' or '\r\n\r\n':
                        continue
                # if not add the message to the request message for s
                    request_message[s] =  request_message[s] + message1
                    message = request_message[s]

                # if it is the end of request, process the request
                
                # add the socket s to the output list for watching writability
                    if s not in outputs:
                        outputs.append(s)




            else:

            # handle the situation where no messages received
                outputs.remove(s)
                inputs.remove(s)
                s.close()
                del request_message[s]

                

    # Handle outputs
    for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
            # No messages need to be sent so stop watching
                outputs.remove(s)
                if s not in inputs:
                    s.close()
                    del message_queues[s]
                    del request_message[s]
            else:
                #print logs and send messages
                print_log(s,message_request,printresponse)
                s.send(message2send.encode())
                
                

    # Handle "exceptional conditions"
    for s in exceptional:
        #print('exception condition on', s.getpeername(),
         #     file=sys.stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
    
    if s not in readable and writable and exceptional:
        #handle timeout events
        socket.settimeout(30)
