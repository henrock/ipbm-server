#IPBM Proof of concept
import PlaySpace
import MissileLauncher
import BodyOfMass
import pygame

import time
import os
import sys
import math

#Creating a few planets
p1 = BodyOfMass.BodyOfMass()
p2 = BodyOfMass.BodyOfMass()
p3 = BodyOfMass.BodyOfMass()
p4 = BodyOfMass.BodyOfMass()
p5 = BodyOfMass.BodyOfMass()
p6 = BodyOfMass.BodyOfMass()

list_of_planets = [p1, p2, p3, p4, p5, p6]

#Assign a starting coordinates
p1.position['x'] = 400
p1.position['y'] = 200
p2.position['x'] = 300
p2.position['y'] = 300
p3.position['x'] = 200
p3.position['y'] = 200
p4.position['x'] = 100
p4.position['y'] = 100
p5.position['x'] = 600
p5.position['y'] = 200
p6.position['x'] = 150
p6.position['y'] = 360


#Assign mass
p1.mass = 1000
p2.mass = 1500
p3.mass = 2000
p4.mass = 3000
p5.mass = 4000
p6.mass = 5000


#Assign raidus
p1.radius = 10
p2.radius = 15
p3.radius = 20
p4.radius = 30
p5.radius = 40
p6.radius = 50

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

#Create font for displaying text
pygame.font.init()
Font = pygame.font.Font(None, 28)

#Check command line arguments
draw_planet_info = False
for text in sys.argv:
    if str(text) == "-Draw_info":
        draw_planet_info = True

#Main loop
while play:
    #Clear screen
    screen.fill((0,0,0))

    #Update time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    elapsed_time = current_time - start_time

    #Upate frame rate
    frame_count += 1;
    frame_sum += delta_time
    if frame_sum > 1:
        frame_rate = flot(frame_count) / frame_sum
        frame_sum = 0
        frame_count = 0
    Text = Font.render("FPS: " + str(int(frame_rate)), True, (255,255,255))

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
                    #Combine them
                    if planet.mass > planet2.mass:
                        planet.mass += planet2.mass
                        planet_area = math.pi * (planet.radius**2)
                        planet2_area = math.pi * (planet2.radius**2)
                        planet.radius = int(math.sqrt(((planet_area + planet2_area) / math.pi)))
                        list_of_planets.remove(planet2)

    #Draw planets
    for planet in list_of_planets:
        pygame.draw.circle(screen,(255,0,255),(int(planet.position['x']), int(planet.position['y'])), planet.radius, 0)

    #Draw FPS
    screen.blit(Text, (10,10))

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

        #Printing information
    if draw_planet_info:
        os.system('cls' if os.name == 'nt' else 'clear')
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
        #print("Time difference is", delta_time)
        print("Elapsed time is ", elapsed_time)
        print("Frame rate is rolling steady at",(int(frame_rate)),"space frames per second")
        print("-------------------------------------------------")

#Finally close the window
pygame.quit()





