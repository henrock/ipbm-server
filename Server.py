#IPBM Server

#IPBM
import PlaySpace
import MissileLauncher
import BodyOfMass

#Network
import socket
import select

#Other
import time
import os
import sys
import math


if __name__ == "__main__":
    #Define a list of clients
    list_of_connections = []

    #Connection information
    host = "localhost"
    port = 9999
    recieve_buffer = 4096

    #Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    #Add server socket to list of connections
    list_of_connections.append(server_socket)

    #Main loop
    run_main_loop = True
    while run_main_loop:
        #List of data to be transmitted
        data_to_be_sent = []

        #Stuff

        #Extra stuff

        #Check connections
        read_sockets, write_sockets, error_sockets = select.select(list_of_connections, [], [])

        for sock in read_sockets:
            #Check for new connections
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                list_of_connections.append(sockfd)
                print("Client (%s, %s) connected" % addr)

            #Check for incoming messages
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(recieve_buffer)

                    #Add recieved data to a send string
                    if data:
                        print("Client wrote: " + data)
                        data_to_be_sent.append(data)
                        sock.send('OK ... ' + data)

                # client disconnected, so remove from socket list
                except:
                    #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    list_of_connections.remove(sock)
                    continue

    server_socket.close()





