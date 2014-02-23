import math
import random
from Particle import *
import sys

VARIANCE = 3 
K = 0.1

class ParticleMCL(Particle):

	def __init__(self, x, y, theta, weight, wall_map):
		Particle.__init__(self, weight)
		self._x = x
		self._y = y
		self._theta = theta
		self._wall_map = wall_map	

	def draw(self):
		return (self._x, self._y, self._theta)

	def calculate_likelihood(self, sensor_distance):
		m = self.calc_min_distance_to_wall()[0]
		z = sensor_distance	
		return math.exp(-math.pow((z - m),2)/(2*VARIANCE)) + K

	def update_weight(self, sensor_distance):
		likelihood = self.calculate_likelihood(sensor_distance)
		self._weight *=	likelihood
		return self._weight

	# don't we need to check we are in the wall?
	def calc_min_distance_to_wall(self):
		ms = self.calc_distances_to_walls()
		for (m, wall) in ms:
			if self.in_wall_of(m, wall):
				return (m, wall)
		return (sys.maxint, wall)

	def calc_distances_to_walls(self):
		return sorted(map(self.calculate_m, self._wall_map))
	
	def to_tuple(self):
		return (self._x, self._y, self._theta, self._weight)

	def calculate_m(self,	(Ax, Ay, Bx, By)):
		x = self._x
		y = self._y
		theta = self._theta
		top = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
		bottom = (By - Ay) * math.cos(math.radians(theta)) - (Bx - Ax) * math.sin(math.radians(theta))
		if (bottom == 0) or (top/bottom) < 0:
			return (sys.maxint, (Ax, Ay, Bx, By))
		else:
			return (top / bottom, (Ax, Ay, Bx, By))    

	def in_wall_of(self, m, (x1, y1, x2, y2)):
		theta = self._theta
		x = self._x + math.cos(math.radians(theta)) * m
		y = self._y + math.sin(math.radians(theta)) * m
		return (min(x1, x2) <= round(x) <= max(x1, x2) and min(y1, y2) <= round(y) <= max(y1, y2))
			
