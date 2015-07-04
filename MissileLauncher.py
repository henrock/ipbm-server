#!/usr/bin/env python
import BodyOfMass

class MissileLauncher:
    launchingVelocity = {'x': 10, 'y': 10}
    parentBody = None

    def launchMissile(self):
        missile = BodyOfMass.BodyOfMass()
        missile.mass = 1
        missile.missileLauncher = self
        missile.position['x'] = self.parentBody.position['x'] + self.launchingVelocity['x'] # förhindra instakrock
        missile.position['y'] = self.parentBody.position['y'] + self.launchingVelocity['y'] # förhindra instakrock
        missile.velocity = self.launchingVelocity
        missile.acceleration = {'x': 0, 'y': 0}
        missile.radius = 1
        missile.name = None
        missile.isControlled = False
        return missile