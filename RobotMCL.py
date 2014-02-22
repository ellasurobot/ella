from collections import Counter
from Robot import *
from ParticleMCL import *
from Sensor import *
import math
import sys
import random

SONAR_DIFFERENCE = 5

class RobotMCL(Robot):
		
	def __init__(self, wall_map, x, y, canvas):
		Robot.__init__(self)
		self._sonar = Sensor("PORT_4", "sonar")
		self._map = wall_map.get_walls()
		self._particles = [ParticleMCL(x, y, 0, (1.0/NUMBER_OF_PARTICLES), self._map) for i in range(NUMBER_OF_PARTICLES)]	
		BrickPiSetupSensors()				#Send the properties of sensors to BrickPi
		self._canvas = canvas

	def draw_particles(self):
		self._canvas.drawParticles([p.to_tuple() for p in self._particles])

	def hittingTheWallIn(self):
		return map(self.get_min_m_for_wall, self._particles)

	def get_min_m_for_wall(self, particle):
		for m in particle.get_m():
			if self.in_wall_of(particle, m):
				return m
		return null

	def sample_particle(self, total_weight):
		sample = random.uniform(0,total_weight)
		temp_weight = 0
		for p in self._particles:
			temp_weight += p.get_weight()
			if (temp_weight >= sample):
				return p

	def get_actual_sonar_value(self):
		readings = []
		while(len(readings) <= 10):
			value = self._sonar.get_value()
			readings.append(value)
		mode = Counter(readings).most_common(1)[0][0]
		print("mode sonar value: ", mode)
		return mode + SONAR_DIFFERENCE

	def resample_particles(self):
		total_weight = 0
		sonar_reading = self.get_actual_sonar_value()
		if sonar_reading < 255:
			for p in self._particles:
				total_weight += p.update_weight(sonar_reading)	
			new_particles = []
			for p in self._particles:
				new_p = self.sample_particle(total_weight)
				new_particles.append(ParticleMCL(new_p.get_x(), new_p.get_y(), new_p.get_theta(), (1.0/NUMBER_OF_PARTICLES), self._map))
			self._particles = new_particles

 	def navigateToWaypoint(self, theta, distance):
		BrickPiUpdateValues()
#		print("turningn : " , theta)
		self.turn(theta)
		time.sleep(0.1)
		self.forward(distance)
#		print("------")
		self.print_stuff()
		self.resample_particles()
		self.print_stuff()
#		print("------")

	def print_stuff(self):
		(x_curr, y_curr, theta_curr) = self.get_current_position()
		print("X_CURR: ", x_curr, "y_curr: ", y_curr, "theta: ", theta_curr)
#		print([(p.get_x(), p.get_y(), p.get_theta(), p.get_weight()) for p in self._particles])

	def navigate_to_way_point_a_bit(self, x, y):
 		(x_curr, y_curr, theta_curr) = self.get_current_position()
 		theta = self.get_degrees_to_turn(x_curr, y_curr, theta_curr, x, y)
#		print("curr", x_curr, y_curr, theta_curr)
		distance = self.get_distance_to_move(x_curr, y_curr, x, y)
		new_distance = min(distance, CYCLE_LENGTH)
		print("Moving distance: ", new_distance, "Rotating degrees", theta)	
		self.navigateToWaypoint(theta, new_distance)
		if(new_distance == CYCLE_LENGTH):
			self.navigate_to_way_point_a_bit(x, y)
		else:
			print("NEW POINT")
			
