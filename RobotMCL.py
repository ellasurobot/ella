from Robot import *
from Sensor import *
import math


class RobotMCL(Robot):
		
	def __init__(self, wall_map):
		Robot.__init__(self)
		self._sonar = Sensor("PORT_4", "sonar")
		self._map = wall_map
		BrickPiSetupSensors()				#Send the properties of sensors to BrickPi

	def hittingTheWallIn(self):
		map(self.get_min_m_for_wall, self._particles)

	def get_min_m_for_wall(self, particle):
		for m in particle.get_m(self._map) :
			if in_wall_of(particle, m):
				return m
		return null

	#need to be moved to some place nice
	def in_wall_of(self, particle, m):
		theta = particle.get_theta()
		x = particle.get_x() + math.cos(math.radians(theta)) * m
		y = particle.get_y() + math.sin(math.radians(theta)) * m
		for (x1, y1, x2, y2) in self._map:
			if (min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)) :
				return True
		return False
