#!/usr/bin/env python

class BodyOfMass:
    def __init__(self):
        self.mass = 0.0
        self.missileLauncher = None
        self.position = { 'x': 0.0, 'y': 0.0 }
        self.velocity = { 'x': 0.0, 'y': 0.0 }
        self.acceleration = { 'x': 0.0, 'y': 0.0 }
        self.radius = 0.0
        self.name = ''
        self.isControlled = False


    # returns a dictionary with x and y values
    def calculateAcceleration(self, list_of_bodies):
        force_x = 0
        force_y = 0
        # calculates the force from each other body
        for body in list_of_bodies:
            if body == self:
                continue
            force_x += self.calculateAccelerationComponent(body, 'x')
            force_y += self.calculateAccelerationComponent(body, 'y')
        if self.mass != 0:
            acceleration_x = force_x / self.mass
            acceleration_y = force_y / self.mass
        return {'x': acceleration_x, 'y': acceleration_y}

    # helpfunction for caclulateAcceleration for one component, returns a force
    def calculateAccelerationComponent(self, body, component):
        if body.position.get(component) != 0:
            e = body.position.get(component) / abs(body.position.get(component)) # unit vector
        else:
            e = 0
        distance = (body.position.get(component) - self.position.get(component))**2
        if distance != 0:
            force = self.mass * body.mass / distance # distance is already squared)
        else:
            force = 0
        return e * force

    # returns a dictionary with x and y values
    def calculateVelocity(self):
        pass

    # returns a dictionary with x and y values
    def calculatePosition(self):
        pass
