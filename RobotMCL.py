from Robot import *
from ParticleMCL import *
from Sensor import *
import math
import sys
import random


class RobotMCL(Robot):
		
	def __init__(self, wall_map, x, y, canvas):
		Robot.__init__(self)
		self._sonar = Sensor("PORT_4", "sonar")
		self._map = wall_map.get_walls()
		self._particles = [ParticleMCL(x, y, (1/NUMBER_OF_PARTICLES), self._map) for i in range(NUMBER_OF_PARTICLES)]	
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
			if (temp_weight > sample):
				return p

	def resample_particles(self):
		total_weight = 0
		for p in self._particles:
			total_weight += p.update_weight(self._sonar.get_value())	
		new_particles = []
		for p in self._particles:
			new_p = self.sample_particle(total_weight)
			new_particles.append(ParticleMCL(new_p.get_x(), new_p.get_y(), (1/NUMBER_OF_PARTICLES), self._map))
		self._particles = new_particles

 	def navigateToWaypoint(self, x, y):
		BrickPiUpdateValues()
		self.resample_particles()
		initial_rotation = self._motorA.get_current_rotation()
 		(x_curr, y_curr, theta_curr) = self.get_current_position()
 		theta = self.get_degrees_to_turn(x_curr, y_curr, theta_curr, x, y)
		print("theta!: ", theta)
		self.turn(theta)
		time.sleep(1)
		distance = self.get_distance_to_move(x_curr, y_curr, x, y)
		self.forward(distance)
		time.sleep(1)
			
		

	#need to be moved to some place nice
	def in_wall_of(self, particle, m):
		theta = particle.get_theta()
		x = particle.get_x() + math.cos(math.radians(theta)) * m
		y = particle.get_y() + math.sin(math.radians(theta)) * m
		print("x: ", x, "y: ", y, "m: ", m)
		for (x1, y1, x2, y2) in self._map:
			if (min(x1, x2) <= round(x) <= max(x1, x2) and min(y1, y2) <= round(y) <= max(y1, y2)) :
				return True
		return False
