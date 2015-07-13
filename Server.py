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
import random

def init_connection():
    #Connection information
    host = ""
    port = 9999

    #Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    #Add server socket to list of connections
    list_of_connections.append(server_socket)

    return server_socket

def get_readable_sockets(connection_list):
    #Check connections that are ready to receive data
    ready_to_read, ready_to_write, in_error = select.select(connection_list, connection_list, connection_list, 0)
    return ready_to_read

def read_incoming_data(server_socket, socket_list, list_of_connections, buffer_size):

    for sock in socket_list:
            # a new connection request received
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                list_of_connections.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast(sockfd, list_of_connections, "[%s:%s] entered our chatting room\n" % addr)

            # a message from a client, not a new connection
            else:
                # process data received from client,
                try:
                    # receiving data from the socket.
                    #print("Received message")
                    data = sock.recv(recieve_buffer)
                    if data:
                        # there is something in the socket
                        decoded_message = data.decode("utf-8")
                        print("Message was:" + decoded_message)
                        broadcast(sock, list_of_connections, '[' + str(sock.getpeername()) + '] ' + decoded_message)
                        #print("Broadcast done.")
                    else:
                        #print("Message was empty, ie connection broken")
                        # remove the socket that's broken
                        if sock in list_of_connections:
                            list_of_connections.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(sock, list_of_connections, "Client (%s, %s) is offline\n" % sock.getpeername())
                        print("Disconnected client (%s:%s)" % sock.getpeername())

                # exception
                except:
                    #print("Exception: Could not receive message.")
                    broadcast(sock, list_of_connections, "Client (%s, %s) is offline\n" % sock.getpeername())
                    print("Client (%s, %s) is offline" % sock.getpeername())
                    continue

def generate_planets(num_planets):
    #Create an empty list
    planet_list = []

    #Generate planets
    for p in range(0, num_planets):
        #Create a planet
        p = BodyOfMass.BodyOfMass()
        p.mass = random.randint(10, 20)
        p.radius = int(p.mass / 2)

        #Create a random velocity
        p.velocity['x'] = random.randint(0, 10)
        p.velocity['y'] = random.randint(0, 10)

        #Randomize position
        p.position['x'] = random.randint(0, 640)
        p.position['y'] = random.randint(0, 480)

        #TODO: Check that the position does not overlap with existing planets

        #Position does not overlap, add the planet to the list
        planet_list.append(p)

    #return the list
    return planet_list

def broadcast (sock, list_of_connections, message):
    for socket in list_of_connections:
        # send the message only to peer
        if socket != server_socket: # and socket != sock :
            try :
                #print("Trying to send message: " + message)
                socket.send(bytes(message, "UTF-8"))
            except :
                print("Failed to send message")
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in list_of_connections:
                    list_of_connections.remove(socket)

def update_planet_positions(planet_list):
    for planet in planet_list:
        #Collision management
        if planet.moving == True:
            #Calculate position
            planet.position['x'] += planet.velocity['x']*time_resolution
            planet.position['y'] += planet.velocity['y']*time_resolution

            #Calculate accelerations
            planet.acceleration = planet.calculateAcceleration(planet_list)

            #Calculate velocity
            planet.velocity['x'] += planet.acceleration['x']*time_resolution
            planet.velocity['y'] += planet.acceleration['y']*time_resolution

def check_planet_collisions(planet_list):
    for planet in planet_list:
        #Check for collisions
        for planet2 in planet_list:
            if planet == planet2:
                continue
            distance = (planet.position['x'] - planet2.position['x'])**2 + (planet.position['y'] - planet2.position['y'])**2
            if distance < (planet.radius + planet2.radius)**2:
                if planet in planet_list:
                    planet_list.remove(planet)
                if planet2 in planet_list:
                    planet_list.remove(planet2)
#                if collision_type == 'merge':
#                    #Merge them
#                    if planet.mass > planet2.mass:
#                        planet.mass += planet2.mass
#                        planet_area = math.pi * (planet.radius**2)
#                        planet2_area = math.pi * (planet2.radius**2)
#                        planet.radius = int(math.sqrt(((planet_area + planet2_area) / math.pi)))
#                        planet_list.remove(planet2)
#                if collision_type == 'remove':
#                    if planet in planet_list:
#                        planet_list.remove(planet)
#                    if planet2 in planet_list:
#                        planet_list.remove(planet2)
#                if collision_type == 'explode':
#                    pass
#                if collision_type == 'bounce':
#                    #sys.exit()
#                    planet.velocity['x'] = (planet.velocity['x'] * planet.mass + planet2.velocity['x'] * planet2.mass) / planet.mass
#                    planet.velocity['y'] = (planet.velocity['y'] * planet.mass + planet2.velocity['y'] * planet2.mass) / planet.mass

def broadcast_planet_positions(planet_list):
    #TODO: Send information
    pass

if __name__ == "__main__":
    #Start server
    print("Server starting")

    #Create a list of planets
    list_of_planets = generate_planets(10)

    #Lists of connections
    list_of_connections = []

    #Send buffer size
    recieve_buffer      = 4096

    #Initialize connection
    server_socket = init_connection()

    #Time variables used to calculate velocity and position
    start_time              = time.time()
    last_time               = time.time()
    current_time            = time.time()
    elapsed_time            = 0
    time_factor             = 1
    rendering_timer         = 0.0
    calculation_timer       = 0.0
    time_resolution         = 0.01
    calculation_tick_limit  = 100           #Physics update limit
    rendering_tick_limit    = 30            #Transmit planet positions to clients limit

    #Tick counting variables
    tick_count  = 0
    tick_sum    = 0
    tick_rate   = 0

    #Main loop
    run_main_loop = True
    while run_main_loop:
        #Check connections for incoming data
        incomming_data_sockets = get_readable_sockets(list_of_connections)

        #Read incoming data
        read_incoming_data(server_socket, incomming_data_sockets, list_of_connections, recieve_buffer)

        #TODO: Check user input

        #Update time
        current_time        = time.time()
        delta_time          = current_time - last_time
        last_time           = current_time
        elapsed_time        = current_time - start_time
        rendering_timer    += delta_time
        calculation_timer  += delta_time

        #Check if its time to update
        if calculation_timer > 1 / calculation_tick_limit / time_factor:
            calculation_timer = 0.0
            #Update tick rate
            tick_count  += 1;
            tick_sum    += delta_time
            if tick_sum > 1:
                tick_rate   = tick_count / tick_sum
                tick_sum    = 0
                tick_count  = 0

            #Update planet positions
            update_planet_positions(list_of_planets)

            #Check for planet collisions
            check_planet_collisions(list_of_planets)

        #Check if its time to send planet positions to clients
        if rendering_timer > 1 / rendering_tick_limit:
            #Send planet positions to clients
            broadcast_planet_positions(list_of_planets)


    #Close all connections
    for sock in list_of_connections:
        socket.close()

    #The end!





