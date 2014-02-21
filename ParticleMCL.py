import math
import random
from Particle import *
import sys

VARIANCE = 3

class ParticleMCL(Particle):

	def __init__(self, x, y, weight, wall_map):
		Particle.__init__(self, weight)
		self._x = x
		self._y = y
		self._wall_map = wall_map	

	def draw(self):
		return (self._x, self._y, self._theta)

	def calculate_likelihood(self, sensor_distance):
		m = self.calc_min_distance_to_wall()
		z = sensor_distance	
		return math.exp(-math.pow((z - m),2)/(2*VARIANCE))

	def update_weight(self, sensor_distance):
		self._weight *= self.calculate_likelihood(sensor_distance)
		return self._weight

	# don't we need to check we are in the wall?
	def calc_min_distance_to_wall(self):
		ms = self.calc_distances_to_walls()
		for m in ms:
			if self.in_wall_of(m):
				return m

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
		#print("x: ", x, "y: ", y, "theta: ", theta)
		#print("Ax: ", Ax, "Ay: ", Ay, "Bx: ", Bx, "By: ", By)
		if (bottom == 0) or (top/bottom) < 0:
			return sys.maxint
		else:
			return top / bottom    

	def in_wall_of(self, m):
		theta = self._theta
		x = self._x + math.cos(math.radians(theta)) * m
		y = self._y + math.sin(math.radians(theta)) * m
		#print("x: ", x, "y: ", y, "m: ", m)
		for (x1, y1, x2, y2) in self._wall_map:
			if (min(x1, x2) <= round(x) <= max(x1, x2) and min(y1, y2) <= round(y) <= max(y1, y2)) :
				return True
		return False
			
