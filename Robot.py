from Motor import *
from MotorSettings import*
from RobotSettings import *
from BrickPi import *
import math

class Robot:
	def __init__(self):
		BrickPiSetup()  # setup the serial port for communication

		self._motorA = Motor("PORT_A") 
		self._motorB = Motor("PORT_B")
		BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

	def forward_simple(self, distance):
		index = self.direction(distance)
		self._motorA.set_speed(FORWARD_SPEED_A*index)
		self._motorB.set_speed(FORWARD_SPEED_B*index)
		BrickPiUpdateValues()
		x = self._motorA.set_initial_rotation()
		degrees_to_turn = abs(distance) * ROTATIONS_PER_CM
		degrees_turned = 0 
		while(degrees_turned < degrees_to_turn):
			degrees_turned = abs(self._motorA.get_current_rotation() - self._motorA.get_initial_rotation())
			BrickPiUpdateValues()

	def direction(self, distance):
		return ((distance)/abs(distance))

	def forward(self, distance):  # distance is in cm
		index = self.direction(distance) 
		self._motorA.set_speed(index * FORWARD_SPEED_A)
		self._motorB.set_speed(index * FORWARD_SPEED_B)
		if (distance > 0):
			self.run_motor(self._motorA, self._motorB, ROTATIONS_PER_CM * math.fabs(distance), "forward")
		else:
			self.run_motor(self._motorA, self._motorB, ROTATIONS_PER_CM * math.fabs(distance), "backward")

	def turn(self, degrees): #degrees in encoder degree
		index = self.direction(degrees) 
		self._motorB.set_speed(index * TURN_SPEED)
		self._motorA.set_speed(-1 * index * TURN_SPEED)
		self.run_motor(self._motorA, self._motorB, ROTATIONS_PER_DEGREE * math.fabs(degrees), "turn")		

	def run_motor(self, reference_motor, other_motor, degrees_to_turn, movement):
		self.error = 0
		BrickPiUpdateValues()
		initial_rotation = reference_motor.update_and_return_initial_rotation()
		other_motor.set_initial_rotation()
		reference_motor.set_start_rotation()
		other_motor.set_start_rotation()
		self.initial_time = time.time()
		init_time = self.initial_time
		while (math.fabs(reference_motor.get_current_rotation() - initial_rotation) < degrees_to_turn):
			if (time.time() - init_time > 0.2):
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
		integral = (reference_motor.get_current_rotation() - reference_motor.get_start_rotation()) - (other_motor.get_current_rotation() - other_motor.get_start_rotation())
		k_p, k_i , k_d = self.get_constants(movement)
		out = k_p * error + k_i * integral + k_d * derivative
		new_speed = int(out + other_motor.get_speed())
		#print("curr speed: ", other_motor.get_speed(),"out: ", out,"error: ", error,"deriv:", derivative,"integral: ", integral,"new speed ", new_speed, "speed_a ", speed_a, "speed_b ", speed_b,"time ", time_difference)
		other_motor.set_speed(new_speed)
		self.error = error

	def get_speed(self, motor, time_difference):
		curr = motor.get_current_rotation() 
		init =  motor.get_initial_rotation()
		rotation_difference = curr - init
		return math.fabs(rotation_difference/time_difference)

	def get_constants(self, movement):
		return {
			"forward": (K_p_f, K_i_f, K_d_f),
			"turn": (K_p_t, K_i_t, K_d_t),
			"backward": (K_p_t, K_i_t, K_d_t)
			}[movement]
