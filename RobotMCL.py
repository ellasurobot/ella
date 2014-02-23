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
			if value < 255:
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
		self.turn(theta)
		time.sleep(0.1)
		self.forward(distance)
		self.print_stuff()
		angle = self.angle_to_wall()
		print("angle: ", angle)
		if (angle < 15):
			self.resample_particles()
		self.print_stuff()

	def print_stuff(self):
		(x_curr, y_curr, theta_curr) = self.get_current_position()
		print("X_CURR: ", x_curr, "y_curr: ", y_curr, "theta: ", theta_curr)

	def navigate_to_way_point_a_bit(self, x, y):
 		(x_curr, y_curr, theta_curr) = self.get_current_position()
 		theta = self.get_degrees_to_turn(x_curr, y_curr, theta_curr, x, y)
		distance = self.get_distance_to_move(x_curr, y_curr, x, y)
		new_distance = min(distance, CYCLE_LENGTH)
		print("Moving distance: ", new_distance, "Rotating degrees", theta)	
		self.navigateToWaypoint(theta, new_distance)
		if(new_distance == CYCLE_LENGTH):
			self.navigate_to_way_point_a_bit(x, y)
		else:
			print("NEW POINT")
			
	def angle_to_wall(self):
		(x_curr, y_curr, theta_curr) = self.get_current_position()
		(Ax, Ay, Bx, By) = self.get_current_wall()
		top = math.cos(math.radians(theta_curr)) * (Ay - By) + math.sin(math.radians(theta_curr)) * (Bx - Ax)
		bottom = math.sqrt(math.pow(Ay - By, 2) + math.pow(Bx - Ax, 2))
		return math.degrees(math.acos(top / bottom))

	def get_current_wall(self):
		wall_list = map(self.find_wall, self._particles)
		return Counter(wall_list).most_common(1)[0][0]
	
	def find_wall(self, particle):
		return particle.calc_min_distance_to_wall()[1]
