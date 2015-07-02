#!/usr/bin/env python

class BodyOfMass:
    def __init__(self):
        self.mass = 0
        self.missileLauncher = None
        self.position = { 'x': 0, 'y': 0 }
        self.velocity = { 'x': 0, 'y': 0 }
        self.acceleration = { 'x': 0, 'y': 0 }
        self.radius = 0
        self.name = ''
        self.isControlled = False


    # returns a dictionary with x and y values
    def calculateAcceleration(self, list_of_bodies):
        # mass of this body
        mass0 = self.mass
        # position of this body
        position0 = self.position
        # x-position of this body
        x0 = self.position.get('x')
        # y-position of this body
        y0 = self.position.get('y')
        # empty list of forces from other bodies
        force_x = 0
        force_y = 0
        # loop that calculates the force from each other body
        # /~----------------------------------------------------~\
        # | Suggestion: line 31-45 can be moved to a new function|
        # \.----------------------------------------------------./
        for body in list_of_bodies:
            # x-position of "the other" body
            x1 = body.position.get('x')
            # y-position of "the other" body
            y1 = body.position.get('y')
            # mass of "the other body"
            mass1 = body.mass
            # distance in x to "the other" body
            distance_x = (x0 - x1)**2
            # distance in y to "the other" body
            distance_y = (y0 - y1)**2
            if distance_x == 0 or distance_y == 0:
                continue
            # force acting on this body (distance is already squared)
            force_x -= mass0 * mass1 / distance_x
            force_y -= mass0 * mass1 / distance_y
        acceleration_x = force_x/mass0
        acceleration_y = force_y/mass0
        return {'x': acceleration_x, 'y': acceleration_y}

    # returns a dictionary with x and y values
    def calculateVelocity(self):
        pass

    # returns a dictionary with x and y values
    def calculatePosition(self):
        pass

