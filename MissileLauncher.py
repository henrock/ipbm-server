#!/usr/bin/env python
import BodyOfMass

class MissileLauncher:

    def __init__(self):
        self.launchingVelocity = {'x': 10, 'y': 10}
        self.parentBody = None

    def launchMissile(self):
        missile = BodyOfMass.BodyOfMass()
        missile.mass = 1
        missile.missileLauncher = self
        missile.position['x'] = self.parentBody.position['x'] + self.parentBody.radius*2 # förhindra instakrock
        missile.position['y'] = self.parentBody.position['y'] + self.parentBody.radius*2 # förhindra instakrock
        print(missile.position)
        missile.velocity = self.launchingVelocity
        missile.acceleration = {'x': 0, 'y': 0}
        missile.radius = 1
        missile.name = None
        missile.isControlled = False
        return missile
