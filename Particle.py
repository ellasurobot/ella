import math
import random

ZOOM_FACTOR = 10
ADJUSTED_DISTANCE = 0

class Particle:

	def __init__(self, weight):
		self._x = ADJUSTED_DISTANCE
		self._y = ADJUSTED_DISTANCE
		self._theta = 0
		self._weight = weight

	def update_distance(self, distance_change):	
		e = self.get_random(0)
		f = self.get_random(0)
		self._x += (distance_change + e) * math.cos(math.radians(self._theta)) * ZOOM_FACTOR
		self._y += (distance_change + e) * math.sin(math.radians(self._theta)) * ZOOM_FACTOR
		self._theta += f
		self._theta %= 360

	def update_rotation(self, theta_change):
		#g = self.get_random(0)
		g = 0
		self._theta += theta_change + g
		self._theta %= 360

	def draw(self):
		return (self._x + 100, self._y + 100, self._theta)

	def get_random(self, n):
		return random.gauss(0, n)
