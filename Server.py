#IPBM Server

#IPBM
import PlaySpace
import MissileLauncher
import BodyOfMass

#Network
import socket
import select
import json

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
    #list_of_connections.append(server_socket)

    return server_socket

def handle_incoming_connections(server_socket, list_of_connections):
    connections = []
    connections.append(server_socket)
    try:
        ready_to_read, ready_to_write, in_error = select.select(connections, [], [], 0)
    except select.error:
        print("Select failed for: handle_incoming_connections")
    # a new connection request received
    for sock in ready_to_read:
        #Accept new connection
        sockfd, addr = server_socket.accept()
        list_of_connections.append(sockfd)
        print("Client (%s, %s) connected" % addr)
        broadcast(list_of_connections, "[%s:%s] entered our chatting room\n" % addr)

def get_readable_sockets(connection_list):
    ready_to_read = []
    #Check that connection_list actually has connections in it
    if len(connection_list) > 0:
        #Check that the connection does not have a bad file descriptor
        for con in connection_list:
            if con.fileno() == -1:
                connection_list.remove(con)
                continue
            #Check connections that are ready to receive data
            #print(connection_list[0])
            ready_to_read, ready_to_write, in_error = select.select(connection_list, [], [], 0)

    return ready_to_read

def get_writable_sockets(connection_list):
    ready_to_write = []
    #Check that connection_list actually has connections in it
    if len(connection_list) > 0:
        #Check that the connection does not have a bad file descriptor
        for con in connection_list:
            if con.fileno() == -1:
                connection_list.remove(con)
                continue
        #Check connections that are ready to transmit data
        ready_to_read, ready_to_write, in_error = select.select([], connection_list, [], 0)
    return ready_to_write


def read_incoming_data(socket_list, connection_list, buffer_size):

    for sock in socket_list:
        # process data received from client,
        try:
            # receiving data from the socket.
            #print("Received message")
            data = sock.recv(recieve_buffer)
            if data:
                # there is something in the socket
                decoded_message = data.decode("utf-8")
                print("Message was: " + decoded_message)
                broadcast(connection_list, '[' + str(sock.getpeername()) + '] ' + decoded_message)
                #print("Broadcast done.")
            else:
                #print("Message was empty, ie connection broken")
                # remove the socket that's broken
                if sock in connection_list:
                    connection_list.remove(sock)

                # at this stage, no data means probably the connection has been broken
                broadcast(connection_list, "Client (%s, %s) is offline\n" % sock.getpeername())
                print("Disconnected client (%s:%s)" % sock.getpeername())

        # exception
        except:
            #broadcast(list_of_connections, "Client (%s, %s) is offline\n" % sock.getpeername())
            print("Exception: could not reveive message")
            socket_list.remove(sock)
            continue

def broadcast (connection_list, message):
    for socket in connection_list:
        #Sen the message to clients only
        if socket != server_socket:
            try :
                socket.send(bytes(message, "UTF-8"))
            except :
                print("Failed to send message to Client (%s, %s)" % socket.getpeername())
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in connection_list:
                    connection_list.remove(socket)

def broadcast_planet_positions_ipbm_encoding(planet_list, list_of_recipients):
    #Prepare empty message
    message = "<BeginPlanets>"

    #Go through the list of connections
    for planet in planet_list:
        #Generate message
        message += str(planet)
        #message += "<Planet position: " + str(int(planet.position["x"])) + ","+ str(int(planet.position["y"])) + ">"
        #message += "<Planet radius: " + str(int(planet.radius)) + ">"

    #End message
    message += "<EndPlanets>"
    #print(message)

    #Send message
    for recipient in list_of_recipients:
        #Do not send to self
        if socket != server_socket:         #Server_socket is defined in the scope of the module that calls this function.
                                            #if this stops working, just add server_socket as a parameter to the function call
            try:
                recipient.send(bytes(message, "UTF-8"))
            except:
                print("Failed to send message to Client (%s, %s)" % recipient.getpeername())
                # broken socket connection
                recipient.close()
                # broken socket, remove it
                if recipient in list_of_recipients:
                    list_of_recipients.remove(recipient)

def broadcast_planet_positions_json_encoding(planet_list, list_of_recipients):
    #Prepare message prefix
    message = "<BeginPlanets>"
    information_list = []
    for planet in planet_list:
        information_list.append((planet.position, planet.radius))

    #Add message data
    message += json.dumps(information_list)

    #End with message suffix
    message += "<EndPlanets>"


    #Send message
    for recipient in list_of_recipients:
        #Do not send to self
        if socket != server_socket:         #Server_socket is defined in the scope of the module that calls this function.
                                            #if this stops working, just add server_socket as a parameter to the function call
            try:
                recipient.send(bytes(message, "UTF-8"))
            except:
                print("Failed to send message to Client (%s, %s)" % recipient.getpeername())
                # broken socket connection
                recipient.close()
                # broken socket, remove it
                if recipient in list_of_recipients:
                    list_of_recipients.remove(recipient)


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

if __name__ == "__main__":
    #Start server
    print("Server starting")

    #Create a list of planets
    list_of_planets         = generate_planets(10)

    #Lists of connections
    list_of_connections     = []

    #Send buffer size
    recieve_buffer          = 4096

    #Initialize connection
    server_socket           = init_connection()

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
    rendering_tick_limit    = 3             #Transmit planet positions to clients limit

    #Tick counting variables
    tick_count  = 0
    tick_sum    = 0
    tick_rate   = 0

    #Main loop
    run_main_loop = True
    while run_main_loop:
        #Check connections for incoming data
        handle_incoming_connections(server_socket, list_of_connections)
        incoming_data_sockets = get_readable_sockets(list_of_connections)

        #Read incoming data
        read_incoming_data(incoming_data_sockets, list_of_connections, recieve_buffer)

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
            #broadcast_planet_positions_ipbm_encoding(list_of_planets, get_writable_sockets(list_of_connections))
            broadcast_planet_positions_json_encoding(list_of_planets, get_writable_sockets(list_of_connections))


    #Close all connections
    for sock in list_of_connections:
        socket.close()

    #The end!





