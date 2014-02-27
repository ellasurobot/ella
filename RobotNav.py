from Robot import *
from Sensor import *

MOTOR_SONAR_SPEED = 50
ROTATION_PER_DEGREE_SONAR = 1

class RobotNav(Robot):
		
	def __init__(self):
		Robot.__init__(self)
		self._motorSonar = Motor("PORT_C") 
		self._sonar = Sensor("PORT_2", "sonar")
		BrickPiSetupSensors()	

	def get_sonar_value(self):
		return self._sonar.get_value()	


	def turn_sonar(self, angle):
		index = angle/abs(angle)
		self._motorSonar.set_speed(index*MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		degrees_to_turn = abs(angle) * ROTATION_PER_DEGREE_SONAR
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()

		while (math.fabs(self._motorSonar.get_current_rotation() - initial_rotation) < degrees_to_turn):
			value = self._sonar.get_value()
			print("sonar, val", value)
			BrickPiUpdateValues()

