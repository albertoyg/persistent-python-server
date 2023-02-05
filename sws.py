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
import os


def processRequest(request):
    requests = request.split('\n')
    for request in requests:
        if re.search(re.compile(r"GET /.* HTTP/1.0"), request):
            if re.search(re.compile(r"connection:\s*Keep-alive", re.IGNORECASE), requests[+1]):
                x =1 
                # handle keeping alive
            else:
                # honour request then close connection
                # if found: print contents 
                # else: return not fund 
                x = 1



def checkMULTImessages():
    messages = message1.split('\n\n')

    # First check if bad requests

    f1 = re.compile(r"GET /.* HTTP/1.0")
    f2 = re.compile(r"connection:\s*Keep-alive", re.IGNORECASE)
    f3 = re.compile(r"connection:\s*close", re.IGNORECASE)

    for message in messages:
        if message == '':
            print('doneeeee')

                        # outputs.remove(s)
                        # inputs.remove(connections)
                        # connection.close()

        elif not re.search(f1, message) and not re.search(f2, message) and not re.search(f3, message):
            bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
            message_queues[connection].put(bad_request)
            curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
            messageCutUp = message.split('\n')
            log = "{time}: {ipport} {req}: {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = bad_request)
            print(log)
                        # cut connection

                        # outputs.remove(connection)
                        # inputs.remove(connections)
                        # connection.close()

                    # good requests
        else:
            print('good req')


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

# Sockets from wchich we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

# request message
request_message = {}

requestLine = []

ipandport = "{ip}:{port}".format(ip = sys.argv[1], port = serverPort)

timeout = 30

lastmessage = 'not empty'

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
                if message1.count('\n') != 1:
                    checkMULTImessages()
                else:
                    # check if message is empty
                    if lastmessage == '\n':
                        if message1 == '\n':
                            print('done single messages')
                            processRequest(request_message[connection])


                    request_message[connection] = request_message[connection] + message1

                    lastmessage = message1
                # if message1[-2:] == ('\n\n'):
                #     checkmessages()

                # messages = message1.split('\n\n')
               

                # # First check if bad requests

                # f1 = re.compile(r"GET /.+ HTTP/1.0")
                # f2 = re.compile(r"GET /.+ HTTP/1.0\nConnection:Keep-alive")
                # f3 = re.compile(r"GET /.+ HTTP/1.0\nConnection: keep-alive")

                # for message in messages:
                #     if message == '':
                #         print('doneeeee')

                #         # outputs.remove(s)
                #         # inputs.remove(connections)
                #         # connection.close()

                #     elif not re.search(f1, message) and not re.search(f2, message) and not re.search(f3, message):
                #         bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
                #         message_queues[connection].put(bad_request)
                #         curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
                #         messageCutUp = message.split('\n')
                #         log = "{time}: {ipport} {req}: {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = bad_request)
                #         print(log)
                #         # cut connection

                #         # outputs.remove(connection)
                #         # inputs.remove(connections)
                #         # connection.close()

                #     # good requests
                #     else:
                #     # add the message to the request message for s
                #         request_message[s] =  request_message[s] + message
                #         decode = message.split()
                #         filename = decode[1][1:]
                #         found = (os.path.isfile(filename))
                #         if not found:
                #             if len(decode) >= 4:
                #                 status = decode[-1].split(':')
                #                 if status[-1] == 'keep-alive' or ' keep-alive':
                #                     not_found_alive = 'HTTP/1.0 404 Not Found\r\nConnection: keep-alive\r\n\r\n'
                #                     sm = 'HTTP/1.0 404 Not Found'
                #                     message_queues[connection].put(not_found_alive)
                #                     curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
                #                     messageCutUp = message.split('\n')
                #                     log = "{time}: {ipport} {req}; {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = sm)
                #                     print(log)
                #                 else:
                #                     not_found = 'HTTP/1.0 404 Not Found\r\nConnection: close\r\n\r\n'
                #                     sm = 'HTTP/1.0 404 Not Found'
                #                     message_queues[connection].put(not_found)
                #                     curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
                #                     messageCutUp = message.split('\n')
                #                     log = "{time}: {ipport} {req}; {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = sm)
                #                     print(log)
                #                     # close
                #         else:
                #             if len(decode) >= 4:
                #                 status = decode[-1].split(':')
                #                 if status[-1] == 'keep-alive' or ' keep-alive':
                #                     ok = 'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\n\r\n'
                #                     sm = 'HTTP/1.0 200 OK'
                #                     message_queues[connection].put(ok)   
                #                     curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
                #                     messageCutUp = message.split('\n')
                #                     log = "{time}: {ipport} {req}; {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = sm)
                #                     print(log)                                                                                                                                                   
                #                 else:
                #                     ok = 'HTTP/1.0 200 OK\r\n\r\n'
                #                     message_queues[connection].put(ok)
                #                     curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
                #                     messageCutUp = message.split('\n')
                #                     log = "{time}: {ipport} {req}; {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = ok)
                #                     print(log)
                #                     # close connection
                #             else:
                #                 ok = 'HTTP/1.0 200 OK\r\n\r\n'
                #                 message_queues[connection].put(ok)
                #                 curtime = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
                #                 messageCutUp = message.split('\n')
                #                 log = "{time}: {ipport} {req}; {res}".format(time = curtime, ipport = ipandport, req = messageCutUp[0], res = ok)
                #                 print(log)
                #                 # close connection
                #             HTMLfile = open(filename, 'r')
                #             message_queues[connection].put(HTMLfile.read())

                # # if it is the end of request, process the request
                
                # # add the socket s to the output list for watching writability
                # if connection not in outputs:
                #     outputs.append(connection)




            else:

            # handle the situation where no messages received
                outputs.remove(connection)
                inputs.remove(connection)
                connection.close()
                del request_message[s]

                

    # Handle outputs
    for s in writable:
            try:
                next_msg = message_queues[connection].get_nowait()
            except queue.Empty:
            # No messages need to be sent so stop watching
                outputs.remove(s)
                if s not in inputs:
                    s.close()
                    del message_queues[s]
                    del request_message[s]
            else:
                s.send(next_msg.encode())

                
                

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
    
    # if s not in readable and writable and exceptional:
    #     #handle timeout events
    #     socket.settimeout(30)

