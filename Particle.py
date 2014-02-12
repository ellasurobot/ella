import math

ZOOM_FACTOR = 10
ADJUSTED_DISTANCE = 100

class Particle:

	def __init__(self, weight):
		self._x = ADJUSTED_DISTANCE
		self._y = ADJUSTED_DISTANCE
		self._theta = 0
		self._weight = weight

	def update_distance(self, distance_change, theta_change):	
		self._x += (distance_change) * math.cos(math.radians(self._theta)) * ZOOM_FACTOR
		self._y += (distance_change) * math.sin(math.radians(self._theta)) * ZOOM_FACTOR
		self._theta += theta_change
		self._theta %= 360
		print str(self.draw())

	def update_rotation(self, theta_change):
		self._theta += theta_change
		self._theta %= 360
		print str(self.draw())

	def draw(self):
		return (self._x, self._y, self._theta)

