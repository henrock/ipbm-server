#!/usr/bin/env python

class MissileLauncher:
	launchingVelocity = {'x': 10, 'y': 10}
	parentBody = None
	
	def launchMissle(self):
		missile = new BodyOfMass()
		missile.mass = 1
		missile.missileLauncher = self
		missile.position = self.parentBody.position
		missile.velocity = self.launchingVelocity
		missile.acceleration = {'x': 0, 'y': 0}
		missile.radius = 0
		missile.name = None
		missile.isControlled = False
		
		return missile