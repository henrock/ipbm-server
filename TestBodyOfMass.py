#IPBM Proof of concept
import PlaySpace
import MissileLauncher
import BodyOfMass
import pygame

import time
import os

#Creating a few planets
p1 = BodyOfMass.BodyOfMass()
p2 = BodyOfMass.BodyOfMass()
p3 = BodyOfMass.BodyOfMass()
list_of_planets = [p1, p2, p3]

#Assign a starting coordinates
p1.position['x'] = 400
p1.position['y'] = 200
p2.position['x'] = 300
p2.position['y'] = 300
p3.position['x'] = 200
p3.position['y'] = 200

#Assign mass
p1.mass = 100
p2.mass = 150
p3.mass = 200

#Assign raidus
p1.radius = 10
p2.radius = 15
p3.radius = 20

#Control variable
play = True

#Time variables used to calculate velocity and position
start_time = time.time()
last_time = time.time()
current_time = time.time()
elapsed_time = 0
#Frame counting variables
frame_count = 0
frame_sum = 0
frame_rate = 0

#Create window and display it
(win_x, win_y) = (640, 480)
screen = pygame.display.set_mode((win_x,win_y))
pygame.display.set_caption('Test')
pygame.display.flip()

#Main loop
while play:
    #Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    screen.fill((0,0,0))

    #Printing information
    print("-------------------------------------------------")
    print("Planet p1 has position     x = ", p1.position['x'])
    print("Planet p1 has position     y = ", p1.position['y'])
    print("Planet p1 has velocity     x = ", p1.velocity['x'])
    print("Planet p1 has velocity     y = ", p1.velocity['y'])
    print("Planet p1 has acceleration x = ", p1.acceleration['x'])
    print("Planet p1 has acceleration y = ", p1.acceleration['y'])
    print("")
    print("Planet p2 has position     x = ", p2.position['x'])
    print("Planet p2 has position     y = ", p2.position['y'])
    print("Planet p2 has velocity     x = ", p2.velocity['x'])
    print("Planet p2 has velocity     y = ", p2.velocity['y'])
    print("Planet p2 has acceleration x = ", p2.acceleration['x'])
    print("Planet p2 has acceleration y = ", p2.acceleration['y'])
    print("")
    print("Planet p3 has position     x = ", p3.position['x'])
    print("Planet p3 has position     y = ", p3.position['y'])
    print("Planet p3 has velocity     x = ", p3.velocity['x'])
    print("Planet p3 has velocity     y = ", p3.velocity['y'])
    print("Planet p3 has acceleration x = ", p3.acceleration['x'])
    print("Planet p3 has acceleration y = ", p3.acceleration['y'])
    print("")

    #Update time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    elapsed_time = current_time - start_time
    #print "Time difference is", delta_time
    print("Elapsed time is ", elapsed_time)
    
    #Upate frame rate
    frame_count += 1;
    frame_sum += delta_time
    
    if frame_count == 10:
        frame_rate = 1 / (frame_sum / 10)
        frame_sum = 0
        frame_count = 0
    
    print("Frame rate is rolling steady at",(int(frame_rate)),"space frames per second")
    
    
    #print "Iterations is ", play

    for planet in list_of_planets:
        #Collision management
        if planet.moving == True:
            #Calculate position
            planet.position['x'] += planet.velocity['x']*delta_time
            planet.position['y'] += planet.velocity['y']*delta_time

            #Calculate accelerations
            planet.acceleration = planet.calculateAcceleration(list_of_planets)

            #Calculate velocity
            planet.velocity['x'] += planet.acceleration['x']*delta_time
            planet.velocity['y'] += planet.acceleration['y']*delta_time

            #Check for collisions
            for planet2 in list_of_planets:
                if planet == planet2:
                    continue
                distance = (planet.position['x'] - planet2.position['x'])**2 + (planet.position['y'] - planet2.position['y'])**2
                if distance < (planet.radius + planet2.radius)**2:
                    #We have a collision, do not update position
                    print("Collision detected!")
                    planet.moving = False

    #Draw planets
    for planet in list_of_planets:
        pygame.draw.circle(screen,(255,0,255),(int(planet.position['x']), int(planet.position['y'])), planet.radius, 0)

    #Update screen
    pygame.display.flip()

    #Check for events
    for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	      play = False
    #Check for keys
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        play = False

    print("-------------------------------------------------")



#Finally close the window
pygame.quit()





