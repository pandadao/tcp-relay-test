# -*- coding:utf-8 -*-
# Author: pandadao

import sys
import socket, thread


MSG_SIZE = 4096

def usage():
    print "Usage: ./relayserver [0.0.0.0 or localhost] [port]"
    sys.exit(1)

# 1. create a new socket connection
# 2. input is hostIP and hostPORT
# 3. output is a socket or error messsage
def Create_Socket(hostIP, hostPORT):
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((hostIP, hostPORT))
        s.listen(5)

    except socket.error, (value, message):
        if s:
            s.close()
            print "Could not open socket: " + messsage
            sys.exit(1)
    return s



# handle the echo server request
def handle_Connection(echosocket, relayIP, relayPort):

    # set parameter for connection
    peerIP = relayIP
    peerPort = relayPort + 1

    # Create new connection
    peersocket = Create_Socket(peerIP, peerPort)

    # send the message back to the echoserver
    peer_msg = peerIP + ":" + str(peerPort)
    echosocket.send(peer_msg)

    #Accept the request
    peerclient, peerclientaddr = peersocket.accept()

    running = 1
    while running:
        # Recieve data from peer client
        peerclientdata = peerclient.recv(MSG_SIZE);
        if peerclientdata:
            # Forward data to echo server
            echosocket.send(peerclientdata)
            # Recieve replay back from echo server
            echoserverdata = echosocket.recv(MSG_SIZE)
            if echoserverdata:
                # Froward replay back to peer client
                peerclient.send(echoserverdata)

            else:
                running = 0

        else:
            running = 0

    peersocket.close()
    echosocket.close()

# Method to create a new relay server
def Relay_Server(relayIP, relayPort):
    relaysocket = Create_Socket(relayIP, relayPort)

    running = 1
    while running:
        # Accept the cpnnectopm
        echosocket, echoaddr = relaysocket.accept()

        # generate a new connection
        thread.start_new_thread(handle_Connection, (echosocket, relayIP, relayPort))

if __name__ == '__main__':

    # Check command line arguments
    total = len(sys.argv)
    if total < 3:
        usage()
    host = sys.argv[1]
    port  = int(sys.argv[2])
    if not port:

    Relay_Server(host, port)
