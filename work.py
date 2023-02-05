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

def checkForFile(requestline):
    decode = requestline.split()
    filename = decode[1][1:]
    return (os.path.isfile(filename), filename)

def processRequest(request):
    requests = request.split('\n')
    checkMULTImessages(requests)
    # for request in requests:
    #     if re.search(re.compile(r"GET /.* HTTP/1.0"), request):
    #         if re.search(re.compile(r"connection:\s*Keep-alive", re.IGNORECASE), requests[+1]):
    #             # handle keeping alive
    #             x = 1
    #         else:
    #             x  = 1 
            # honour request then close connection
                # if found: print contents 
                # else: return not fund 



def checkMULTImessages(messages):

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
                    message_queues[s].put(ok)
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
                    message_queues[s].put(not_found)
                #   BUT FOR NOW....
                    print(not_found)
            else:
            # check for bad header line
                if not re.search(re.compile(r"connection:\s*close", re.IGNORECASE), messages[curRequest+1]) and messages[curRequest + 1] != '':
                # if we are here, the header line is bad
                    bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
                #   PRINT notfound MESSAGE TO CLIENT 
                    message_queues[s].put(bad_request)
                #   BUT FOR NOW....
                    outputs.remove(s)
                    inputs.remove(connection)
                    s.close()
        # if connection: closed, check if file exists 
                found, filename = checkForFile(messages[curRequest])
                if found: 
                    ok = 'HTTP/1.0 200 OK\r\n\r\n'
                #   PRINT OK MESSAGE TO CLIENT 
                    message_queues[s].put(ok)
                #   BUT FOR NOW....
                    print(ok)
                # output file contents 
                    HTMLfile = open(filename, 'r')
                #   PRINT file contents TO CLIENT 
                    message_queues[s].put(HTMLfile.read())
                #   BUT for now....
                    print(HTMLfile.read())

                # CLOSE CONNECTION
                    outputs.remove(s)
                    inputs.remove(connection)
                    s.close()
                else:
        #       # file not found
                    not_found = 'HTTP/1.0 404 Not Found\r\nConnection: close\r\n\r\n'
                #   PRINT notfound MESSAGE TO CLIENT 
                    message_queues[s].put(not_found)
                #   BUT FOR NOW....
                    print(not_found)
            
                # CLOSE CONNECTION
                    outputs.remove(s)
                    inputs.remove(connection)
                    s.close()

    # check if end of requests: \n\n
        elif messages[curRequest] == '':
        # empty line detected
            if curRequest + 1 < len(messages):
            # check if it's last line
                if messages[curRequest + 1] == '':
                # if we are here, last two lines are empty
                    outputs.remove(s)
                    inputs.remove(connection)
                    s.close()
                    
    # BAD REQUEST  
        else:
        # ensure it's not the header
            if not re.search(re.compile(r"connection:\s*Keep-alive", re.IGNORECASE), messages[curRequest]) and not re.search(re.compile(r"connection:\s*close", re.IGNORECASE), messages[curRequest]) and messages[curRequest] != '':
                bad_request = 'HTTP/1.0 400 Bad Request\r\n\r\n'
            #   PRINT notfound MESSAGE TO CLIENT 
                message_queues[s].put(bad_request)
            #   BUT FOR NOW....
                outputs.remove(s)
                inputs.remove(connection)
                s.close()

                print(bad_request)



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
            # outputs.append(s)
            request_message[connection] = "" # OR queue
            #new_request[s] = True
            #persistent_socket[connection] = True
            # Give the connection a queue for data
            # we want to send
            message_queues[connection] = queue.Queue()

        else:
            message1 =  s.recv(1024).decode()
            if message1:   
                if message1.count('\n') != 1:
                    if s not in outputs:
                        outputs.append(s)
                    checkMULTImessages(message1.split('\n'))
                else:
                    # check if message is empty
                    if lastmessage == '\n':
                        if message1 == '\n':
                            print('done single messages')
                            if s not in outputs:
                                outputs.append(s)
                            processRequest(request_message[s])


                    request_message[s] = request_message[s] + message1

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

