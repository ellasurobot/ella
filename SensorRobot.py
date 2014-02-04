from Motor import *
from MotorSettings import*
from RobotSettings import *
from Robot import *
from Sensor import *
import math

class SensorRobot(Robot):

		def __init__(self):
				Robot.__init__(self)
				self._left_touch = Sensor("PORT_2", "touch")
				self._right_touch = Sensor("PORT_4", "touch")
				self._sonar = Sensor("PORT_1", "sonar")
				BrickPiSetupSensors()				#Send the properties of sensors to BrickPi

		def forward_touch_sensor(self):
				while(True):
					self._motorA.set_speed(FORWARD_SPEED_A)
					self._motorB.set_speed(FORWARD_SPEED_B)
					left_bumped = self._left_touch.get_value()
					right_bumped = self._right_touch.get_value()
					if (left_bumped and right_bumped):
						self.forward(-10)
						self.turn(90)
					elif (left_bumped):
						self.forward(-10)
						self.turn(90)
					elif (right_bumped):
						self.forward(-10)
						self.turn(-90)
					BrickPiUpdateValues()
								
		def forward_bump(self, bump_distance):
				print("buuuuuuuuuuump")
