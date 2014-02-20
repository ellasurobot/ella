import math
import random
from Particle import *
import sys

ADJUSTED_DISTANCE = 0
VAR_DISTANCE_FOR_FORWARD_PER_CM = 0.2
VAR_TURN_FOR_FORWARD_PER_CM = 0.5
VAR_TURN_FOR_TURN_PER_CM = 0.005

class ParticleMCL(Particle):

	def __init__(self, x, y, weight, wall_map):
		Particle.__init__(self, weight)
		self._x = x
		self._y = y
		self._wall_map = wall_map	

	def draw(self):
		return (self._x, self._y, self._theta)

	def calculate_likelihood(x, y, theta, z):
		pass

	def get_m(self):
		return sorted(map(self.calculate_m, self._wall_map))

	
	def to_tuple(self):
		return (self._x, self._y, self._theta, self._weight)

	def calculate_m(self,	wall):
		Ax = wall[0]
		Ay = wall[1]
		Bx = wall[2]
		By = wall[3] 
		x = self._x
		y = self._y
		theta = self._theta
		top = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
		bottom = (By - Ay) * math.cos(math.radians(theta)) - (Bx - Ax) * math.sin(math.radians(theta))
		print("x: ", x, "y: ", y, "theta: ", theta)
		print("Ax: ", Ax, "Ay: ", Ay, "Bx: ", Bx, "By: ", By)
		print("top: ", top, "Botoom: ", bottom, "result: ", top/bottom)
		if (bottom == 0) or (top/bottom) < 0:
			return sys.maxint
		else:
			return top / bottom    
