import math

ZOOM_FACTOR = 10

class Particle:

	def __init__(self, weight):
		self._x = 50
		self._y = 50
		self._theta = 0
		self._weight = weight

	def update_distance(self, distance_change, theta_change):	
		self._x += (distance_change) * math.cos(math.radians(self._theta)) * ZOOM_FACTOR
		self._y += (distance_change) * math.sin(math.radians(self._theta)) * ZOOM_FACTOR
		self._theta += theta_change

	def update_rotation(self, theta_change):
		self._theta += theta_change

	def draw(self):
		return (self._x, self._y, self._theta)

