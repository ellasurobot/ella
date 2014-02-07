from Motor import * 
from MotorSettings import*
from RobotSettings import *
from Robot import *
from Sensor import *
import math, time

MIN_SPEED = 80
K_SONAR = 3
K_WALL = 2
DISTANCE_TRESHOLD = 50
ARRAY_LENGTH = 15

class SensorRobot(Robot):

		def __init__(self):
				Robot.__init__(self)
				self._left_touch = Sensor("PORT_2", "touch")
				self._right_touch = Sensor("PORT_4", "touch")
				self._sonar = Sensor("PORT_1", "sonar")
				self.error = 0
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
				actual_distance = self.__get_mean_distance(prev_values)
				time.sleep(.01)
				BrickPiUpdateValues()	

		def wall_walking_2(self, distance):
			self._motorA.set_speed(120)
			self._motorB.set_speed(130)
			self.set_recover_speed_2(0)
			K = 2
			while(True):
				if(True):
					BrickPiUpdateValues()
					curr_distance = self._sonar.get_value()
					diff = curr_distance - distance
#					diff = math.copysign(min(abs(diff), 4),diff)
					print("distance: ", curr_distance ," diff: ", diff)
					print("speed_A: ", self._motorA.get_speed(), "speed b: ", self._motorB.get_speed()) 
					print()
					if(curr_distance < 200):
						if(diff != 0):
							self.set_recover_speed_2(K * diff)
							prev_time = time.time()
							prev_distance = distance


		

		def set_recover_speed_2(self, speed):
			self._motorA.set_speed(120 - speed)
			self._motorB.set_speed(130 + speed)
			BrickPiUpdateValues()	

				
		def wall_walking(self, distance):
			BrickPiUpdateValues()
			actual_distance = self._sonar.get_value()
			prev_values = [actual_distance]
			self.set_recover_speed(0)
			while(True):
				walk_time = time.time()
				speed = K_WALL * (actual_distance - distance)
				if(abs(speed) > 4):
					self.set_recover_speed(speed)
					print("speed_a", self._motorA.get_speed(), "speed_b", self._motorB.get_speed(), "distance", actual_distance, "sonar", self._sonar.get_value(), "speed", speed)
					print("START WAIT\n")
					while(time.time() - walk_time < 0.2):
						pass
					print("END WAIT\n")
					walk_time = time.time()
					self.set_recover_speed(-speed)
					print("speed_a", self._motorA.get_speed(), "speed_b", self._motorB.get_speed(), "distance", actual_distance, "sonar", self._sonar.get_value(), "speed", speed)
#				while(time.time() - walk_time < 0.2):
#					pass
				prev_values = self.__get_prev_values(prev_values, self._sonar.get_value())
				actual_distance = prev_values[len(prev_values)-1]
				BrickPiUpdateValues()

		def set_recover_speed(self, speed):
			self._motorA.set_speed(FOLLOW_WALL_SPEED - speed)
			self._motorB.set_speed(FOLLOW_WALL_SPEED + speed)
			BrickPiUpdateValues()	


		def __get_prev_values(self, prev_values, value):
			if(value < prev_values[len(prev_values) -1] + DISTANCE_TRESHOLD):
				if(len(prev_values) >= ARRAY_LENGTH):
					prev_values.pop(0)
				prev_values.append(value)
				#print("prev_values", prev_values)
			return prev_values

		def __get_mean_distance(self, prev_values):
			return sum(prev_values)/len(prev_values)				

	
