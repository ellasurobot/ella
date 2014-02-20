from Robot import *
from ParticleMCL import *
from Sensor import *
import math
import sys


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
