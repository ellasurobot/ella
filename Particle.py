import math 
import random
from DrawSquare import *
import sys
from Robot import *
import globals

VAR_DISTANCE_FOR_FORWARD_PER_CM = 0.015 # 0.15
VAR_TURN_FOR_FORWARD_PER_CM = 0.04 # 0.02 # 0.01
VAR_TURN_FOR_TURN_PER_CM = 0.01 # 0.01 # 0.01

class Particle:

	def __init__(self, weight):
		self._x = 0
		self._y = 0
		self._theta = 0
		self._weight = weight

	def update_distance(self, distance_change):	
		var_distance = VAR_DISTANCE_FOR_FORWARD_PER_CM*math.pow(distance_change,2)
#		if(globals.VAR_BIG):
#			var_distance *= 2
		var_turn = VAR_TURN_FOR_FORWARD_PER_CM*math.pow(distance_change,2)
		e = self.get_random(var_distance)
		f = self.get_random(var_turn)
#		if(globals.BIG_ANGLE or globals.BAD):
#			e *= 0.5
#			f *= 0.5
#			e = f = 0
		self._x += (distance_change + e) * math.cos(math.radians(self._theta))
		self._y += (distance_change + e) * math.sin(math.radians(self._theta))
		self._theta += f

	def update_rotation(self, theta_change):
#		g = 0
		var_turn = VAR_TURN_FOR_TURN_PER_CM*math.pow(theta_change,2)
		g = self.get_random(var_turn)
#		if(globals.BIG_ANGLE or globals.BAD):
#			g = 0
#			g *= 0.5
		self._theta += theta_change + g

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
