import math

class Particle:

	def __init__(self):
		self._x = 0
		self._y = 0
		self._theta = 0

	def update_distance(self, distance_change, theta_change):	
		self._x += (distance_change) * math.cos(self._theta)
		self._y += (distance_change) * math.sin(self._theta)
		self._theta += theta_change

	def update_rotation(self, theta_change):
		self._theta += theta_change

	def draw(self):
		return (self._x, self._y, self._theta)

