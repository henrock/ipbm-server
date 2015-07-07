#!/usr/bin/env python
import BodyOfMass
import math

class MissileLauncher:

    def __init__(self):
        self.launchingVelocity = {'x': 10, 'y': 10}
        self.parentBody = None

    def launchMissile(self, mouse_position):
        missile = BodyOfMass.BodyOfMass()
        missile.acceleration = {'x': 0, 'y': 0}
        missile.radius = 1
        missile.name = None
        missile.isControlled = False
        missile.mass = 1
        missile.missileLauncher = self
        mouse_x = mouse_position[0]
        body_x = self.parentBody.position['x']
        mouse_y = mouse_position[1]
        body_y = self.parentBody.position['y']
        length = math.sqrt((mouse_x - body_x)**2 + (mouse_y - body_y)**2)
        launch_x = (mouse_x - body_x) / length * (self.parentBody.radius + 2) + body_x
        launch_y = (mouse_y - body_y) / length * (self.parentBody.radius + 2) + body_y
        missile.position['x'] = launch_x
        missile.position['y'] = launch_y
        missile.velocity['x'] = (mouse_x - body_x) / length * self.parentBody.radius
        missile.velocity['y'] = (mouse_y - body_y) / length * self.parentBody.radius
        return missile