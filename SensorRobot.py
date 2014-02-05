from Motor import * 
from MotorSettings import*
from RobotSettings import *
from Robot import *
from Sensor import *
import math

MIN_SPEED = 80
K_SONAR = 3
DISTANCE_TRESHOLD = 50
ARRAY_LENGTH = 15

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
						self.forward_simple(-10)
						self.turn(90)
					elif (left_bumped):
						self.forward_simple(-10)
						self.turn(90)
					elif (right_bumped):
						self.forward_simple(-10)
						self.turn(-90)
					BrickPiUpdateValues()
								
		def forward_sonar(self, distance):
			BrickPiUpdateValues()
			actual_distance = self._sonar.get_value()
			prev_values = [actual_distance]
			print("actual dist", actual_distance)
			while(True):
				if(actual_distance > distance):
					speed = K_SONAR * (actual_distance - distance) + MIN_SPEED
					print("sonar distance", self._sonar.get_value(), "actual dist", actual_distance, "speed: ", speed)
				elif abs(actual_distance - distance) <= 1:
					speed = 0
				else:
					speed = K_SONAR * (actual_distance - distance) - MIN_SPEED
				self._motorA.set_speed(speed)
				self._motorB.set_speed(speed)
				prev_values = self.__get_prev_values(prev_values, self._sonar.get_value())
				actual_distance = self.__get_median_distance(prev_values)
				time.sleep(.01)
				BrickPiUpdateValues()	

		def __get_prev_values(self, prev_values, value):
			if(value < prev_values[len(prev_values) -1] + DISTANCE_TRESHOLD):
				if(len(prev_values) >= ARRAY_LENGTH):
					prev_values.pop(0)
				prev_values.append(value)
				#print("prev_values", prev_values)
			return prev_values

		def __get_median_distance(self, prev_values):
			#sorted_values = sorted(prev_values)
			#return sorted_values[len(sorted_values)/2]
			return sum(prev_values)/len(prev_values)				

	
