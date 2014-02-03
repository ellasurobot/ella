from Motor import *
from MotorSettings import*
from RobotSettings import *
import math

class Robot:
	def __init__(self):
		BrickPiSetup()  # setup the serial port for communication

		self.__motorA = Motor("PORT_A") 
		self.__motorB = Motor("PORT_B")

		BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

	def forward(self, distance):  # distance is in cm
		self.__motorA.set_speed(FORWARD_SPEED)
		self.__motorB.set_speed(FORWARD_SPEED)
		self.run_motor(self.__motorA, self.__motorB, ROTATIONS_PER_CM * distance, "forward")

	def turn(self, degrees): #degrees in encoder degree
		index = (degrees - abs(degrees)) + 1
		self.__motorA.set_speed(index * TURN_SPEED)
		self.__motorB.set_speed(-1 * index * TURN_SPEED)
		self.run_motor(self.__motorA, self.__motorB, ROTATIONS_PER_DEGREE * degrees, "turn")		

	def run_motor(self, reference_motor, other_motor, degrees_to_turn, movement):
		self.error = 0
		BrickPiUpdateValues()
		initial_rotation = reference_motor.update_and_return_initial_rotation()
		other_motor.set_initial_rotation()
		reference_motor.set_start_rotation()
		other_motor.set_start_rotation()
		self.initial_time = time.time()
		while (reference_motor.get_current_rotation() - initial_rotation < degrees_to_turn):
			self.adjust_speed(reference_motor, other_motor, self.initial_time, movement)
			BrickPiUpdateValues()

	# Adjust the speed of other motor according to the reference motor
	# using the PID algorithm
	def adjust_speed(self, reference_motor, other_motor, initial_time, movement):
		time_difference = time.time() - initial_time
		if (time_difference > TIME_DIFF):
			self.control(reference_motor, other_motor, time_difference, movement)
			reference_motor.set_initial_rotation()
			other_motor.set_initial_rotation()
			self.initial_time = time.time()

	def control(self, reference_motor, other_motor, time_difference, movement):
		speed_a = self.get_speed(reference_motor, time_difference)
		speed_b = self.get_speed(other_motor, time_difference)
		error = speed_a - speed_b
		derivative = (error - self.error)/time_difference
		print("A: ", reference_motor.get_start_rotation(), "B: ", other_motor.get_start_rotation())
		integral = (reference_motor.get_current_rotation() - reference_motor.get_start_rotation()) - (other_motor.get_current_rotation() - other_motor.get_start_rotation())
		k_p, k_i , k_d = self.get_constants(movement)
		out = k_p * error + k_i * integral + k_d * derivative
		new_speed = int(out + other_motor.get_speed())
		print(k_p, k_i, k_d)
		print("curr speed: ", other_motor.get_speed(),"out: ", out,"error: ", error,"deriv:", derivative,"integral: ", integral,"new speed ", new_speed, "speed_a ", speed_a, "speed_b ", speed_b,"time ", time_difference)
		other_motor.set_speed(new_speed)
		self.error = error

	def get_speed(self, motor, time_difference):
		curr = motor.get_current_rotation() 
		init =  motor.get_initial_rotation()
		rotation_difference = curr - init
		print("curr: ", curr, "init: ", init)
		return rotation_difference/time_difference

	def get_constants(self, movement):
		return {
			"forward": (K_p_f, K_i_f, K_d_f),
			"turn": (K_p_t, K_i_t, K_d_t)
			}[movement]
