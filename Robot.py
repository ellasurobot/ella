from Motor import *
from MotorSettings import*
import math

class Robot:
	def __init__(self):
		BrickPiSetup()  # setup the serial port for communication

		self.__motorA = Motor(PORT_A) 
		self.__motorB = Motor(PORT_B) 

		BrickPiSetupSensors()       #Send the properties of sensors to BrickPi
		BrickPiUpdateValues() 

	def forward(distance):  # distance is in cm
		self.__motorA.set_speed(FORWARD_SPEED_A)
		self.__motorB.set_speed(FORWARD_SPEED_B)
		run_motor(self.__motorA, self.__motorB, ROTATIONS_PER_CM * distance_cm, "forward")

	def turn(degrees): #degrees in encoder degree
		index = (degrees - abs(degrees)) + 1
		self.__motorA.set_speed(index * TURN_SPEED)
		self.__motorB.set_speed(-1 * index * TURN_SPEED_B)
		run_motor(self.__motorA, self.__motorB, ROTATIONS_PER_DEGREE * degrees, "turn")		

	def run_motor(reference_motor, other_motor, degrees_to_turn, movement):
		initial_rotation = reference_motor.update_and_return_initial_rotation()
		initial_time = time.time()
		while (reference_motor.get_current_rotation() - initial_rotation < degress_to_turn):
			adjust_speed(reference_motor, other_motor, initial_time, movement)
			initial_time = time.time()
			BrickPiUpdateValues()

	# Adjust the speed of other motor according to the reference motor
	# using the PID algorithm
	def adjust_speed(reference_motor, other_motor, initial_time, movement):
		time_difference = time.time() - initial_time
		if (time_difference > TIME_DIFF):
			adjustment = control(reference_motor, other_motor, initial_time, movement)
			other_motor.set_speed(other_motor.get_speed() + adjustment)
			reference_motor.update_and_return_initial_rotation()
			other_motor.update_and_return_initial_rotation()

	def control(reference_motor, other_motor, initial_time, movement):
		time_difference = time.time() - initial_time
		speed_a = get_speed(reference_motor)
		speed_b = get_speed(other_motor)
		error = speed_a - speed_b
		derivative = (error - ERROR)/time_difference
		integral = math.fabs(reference_motor.get_current_rotation() - reference_motor.get_initial_rotation()) - math.fabs(other_motor.get_current_rotation() - other_motor.get_initial_rotation())
		k_p, k_i , k_d = get_constants(movement)
		out = k_p * error + k_i * integral + k_d * derivative
		other_motor.set_speed(other_motor.get_speed() + out)
		ERROR = error

	def get_constants(movement):
		return {
			"forward": (K_p_f, K_i_f, K_d_f),
			"turn": (K_p_t, K_i_t, K_d_t)
			}[movement]
