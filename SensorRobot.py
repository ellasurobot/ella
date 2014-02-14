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
ARRAY_LENGTH = 10 

class SensorRobot(Robot):

		def __init__(self):
				Robot.__init__(self)
				self._left_touch = Sensor("PORT_1", "touch")
				self._right_touch = Sensor("PORT_2", "touch")
				self._sonar = Sensor("PORT_4", "sonar")
				self.error = 0
				BrickPiSetupSensors()				#Send the properties of sensors to BrickPi

		def calibrate_sonar(self):
			while(True):
				actual_distance = self._sonar.get_value()
				print("actual_distance:", actual_distance)
				BrickPiUpdateValues()
			

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
				elif abs(actual_distance - distance) <= 1:
					speed = 0
				else:
					speed = K_SONAR * (actual_distance - distance) - MIN_SPEED
				print("sonar distance", self._sonar.get_value(), "actual dist", actual_distance, "speed: ", speed)
				self._motorA.set_speed(speed)
				self._motorB.set_speed(speed)
				prev_values = self.__get_prev_values(prev_values, self._sonar.get_value())
				actual_distance = self.__get_mean_distance(prev_values)
				time.sleep(.01)
				BrickPiUpdateValues()	

		def walking_test(self, distance):
			self.set_recover_speed_2(0)

			correction = 70

			prev_time = time.time()
			while(time.time() - prev_time < 2):
				BrickPiUpdateValues()

			for i in range(0,10):
	
							print("TURN")
							self.set_recover_speed_2(correction)
							prev_time = time.time()
							while(time.time() - prev_time < 0.1):
								BrickPiUpdateValues()
							self.set_recover_speed_2(0)
							print("TURN")
							
							prev_time = time.time()
							while(time.time() - prev_time < 0.2):
								BrickPiUpdateValues()

							self.set_recover_speed_2(-1.2*correction)
							prev_time = time.time()
							while(time.time() - prev_time < 0.1):
								BrickPiUpdateValues()
							self.set_recover_speed_2(0)
							print("DONE")

			prev_time = time.time()
			while(time.time() - prev_time < 1):
				BrickPiUpdateValues()



		def wall_walking_2(self, distance):
			self.set_recover_speed_2(0)
			K = 7 
			while(True):
				BrickPiUpdateValues()
				curr_distance = self._sonar.get_value()
				print("curr_distance: ", curr_distance)
				diff_o = curr_distance - distance
				diff = math.copysign(min(abs(diff_o), 6),diff_o)
				print()
				if(diff != 0):
					correction = K * diff
	#				if(curr_distance < 200):
	#					if(diff != 0):
	#						correction = K * diff
					self.set_recover_speed_2(1.5* correction)
					print("diff: ", diff, "correction: ", correction, "speeda: ", self._motorA.get_speed(), "speedb: ", self._motorB.get_speed())
					prev_time = time.time()
					while(time.time() - prev_time < 0.2):
						BrickPiUpdateValues()
					self.set_recover_speed_2(0)
					prev_time = time.time()
					while(time.time() - prev_time < (0.2 * diff/6)):
						BrickPiUpdateValues()
					interval = 0.2 + 0.1 * diff/6
					self.set_recover_speed_2(-1*correction)
					prev_time = time.time()
					while(time.time() - prev_time < interval):
						BrickPiUpdateValues()
					self.set_recover_speed_2(0)


										
		def set_recover_speed_2(self, speed):
			self._motorA.set_speed(FORWARD_SPEED_A - speed)
			self._motorB.set_speed(FORWARD_SPEED_B + speed)
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
				while(time.time() - walk_time < 0.2):
					pass
				self.set_recover_speed(0)
				prev_values = self.__get_prev_values(prev_values, self._sonar.get_value())
				actual_distance = prev_values[len(prev_values)-1]
				BrickPiUpdateValues()

		def set_recover_speed(self, speed):
			self._motorA.set_speed(FOLLOW_WALL_SPEED - speed)
			self._motorB.set_speed(FOLLOW_WALL_SPEED + speed)
			BrickPiUpdateValues()	


		def __get_prev_values(self, prev_values, value):
		#	if(value < prev_values[len(prev_values) -1] + DISTANCE_TRESHOLD):
			if(len(prev_values) >= ARRAY_LENGTH):
				prev_values.pop(0)
			prev_values.append(value)
			return prev_values

		def __get_mean_distance(self, prev_values):
			sorted_array = sorted(prev_values)
			if (len(prev_values) % 2 == 1):
				return sorted_array[len(prev_values)/2]
			else:
				mid = len(prev_values)/2
				return (sorted_array[mid - 1] + sorted_array[mid])/2
#			return sum(prev_values)/len(prev_values)				

	
