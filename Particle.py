import math
import random
from DrawSquare import *

ADJUSTED_DISTANCE = 0
VAR_DISTANCE_FOR_FORWARD_PER_CM = 0.2
VAR_TURN_FOR_FORWARD_PER_CM = 0.5
VAR_TURN_FOR_TURN_PER_CM = 0.005

class Particle:

	def __init__(self, weight):
		self._x = ADJUSTED_DISTANCE
		self._y = ADJUSTED_DISTANCE
		self._theta = 0
		self._weight = weight

	def update_distance(self, distance_change):	
		var_distance = VAR_DISTANCE_FOR_FORWARD_PER_CM*math.pow(distance_change,2)
		var_turn = VAR_TURN_FOR_FORWARD_PER_CM*math.pow(distance_change,2)
		e = self.get_random(var_distance)
		f = self.get_random(var_turn)
#		e = f =  0
		self._x += (distance_change + e) * math.cos(math.radians(self._theta))
		self._y += (distance_change + e) * math.sin(math.radians(self._theta))
		self._theta += f
		self._theta %= 360

	def update_rotation(self, theta_change):
		#g = self.get_random(0)
		var_turn = VAR_TURN_FOR_TURN_PER_CM*math.pow(theta_change,2)
		g = self.get_random(var_turn)
		self._theta += theta_change + g
		self._theta %= 360

	def calculate_likelihood(x, y, theta, z):
		pass

	def draw(self):
		return (self._x*ZOOM_FACTOR + ORIGIN_X, -self._y*ZOOM_FACTOR + ORIGIN_Y, self._theta)

	def get_random(self, n):
		return random.gauss(0, n)

	def get_x(self):
		return self._x;

	def get_y(self):
		return self._y;

	def get_theta(self):
		return self._theta;

	def get_weight(self):
		return self._weight;

	def get_m(self, wall_map):
		return sort(calculate_m, wall_map)

	def calculate_m(self, wall):
		Ax = wall[0]
		Ay = wall[1]
		Bx = wall[2]
		By = wall[3] 
		x = self._x
		y = self._y
		theta = self._theta
		top = (Bx - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
		bottom = (By - Ay) * math.cos(math.radians(theta)) - (Bx - Ax) * math.sin(math.radians(theta))
		return top / bottom    
