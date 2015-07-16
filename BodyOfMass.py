#!/usr/bin/env python
import math

class BodyOfMass:
    def __init__(self):
        self.mass            = 0.0
        self.missileLauncher = None
        self.position        = { 'x': 0.0, 'y': 0.0 }
        self.velocity        = { 'x': 0.0, 'y': 0.0 }
        self.acceleration    = { 'x': 0.0, 'y': 0.0 }
        self.radius          = 0.0
        self.name            = ''
        self.isControlled    = False
        self.moving          = True

    def assign(pos, rad):
        self.position   = pos
        self.radius     = rad

    # returns a dictionary with x and y values
    def calculateAcceleration(self, list_of_bodies):
        force_x = 0
        force_y = 0
        # calculates the force from each other body
        for body in list_of_bodies:
            if body == self:
                continue
            vector_x = body.position['x'] - self.position['x']
            vector_y = body.position['y'] - self.position['y']
            #print(vector_x, vector_y)
            vector_length = math.sqrt(vector_x**2 + vector_y**2)
            #print(vector_length)
            force = self.mass * body.mass / vector_length
            pointing_vector = self.pointingAt(body)
            #print(pointing_vector)
            force_x += pointing_vector['x'] * force# + self.position['x']
            force_y += pointing_vector['y'] * force# + self.position['y']
        return {'x': force_x, 'y': force_y}

    # returns a dictionary with x and y values
    def calculateVelocity(self):
        pass

    # returns a dictionary with x and y values
    def calculatePosition(self):
        pass

    # helpfunctions
    # returns a vector pointing from self to body
    def pointingAt(self, body):
        vector_x      = body.position['x'] - self.position['x']
        vector_y      = body.position['y'] - self.position['y']
        vector_length = math.sqrt(vector_x**2 + vector_y**2)
        normal_x      = vector_x / vector_length
        normal_y      = vector_y / vector_length
        return {'x': normal_x, 'y': normal_y}
