from Motor import *
from MotorSettings import*
from RobotSettings import *
from BrickPi import *
from Particle import*
import math
from operator import attrgetter

NUMBER_OF_PARTICLES = 1

class Robot:
	def __init__(self):
		BrickPiSetup()  # setup the serial port for communication
		self._particles = [Particle(1.0/NUMBER_OF_PARTICLES) for i in range(NUMBER_OF_PARTICLES)]
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
		while(degrees_turned < degrees_to_turn - 20):
			degrees_turned = abs(self._motorA.get_current_rotation() - self._motorA.get_initial_rotation())
			BrickPiUpdateValues()

	def direction(self, distance):
		return 1 if distance == 0 else ((distance)/abs(distance))

	def forward(self, distance):  # distance is in cm
		index = self.direction(distance) 
		self._motorA.set_speed(index * FORWARD_SPEED_A)
		self._motorB.set_speed(index * FORWARD_SPEED_B)
		if (distance > 0):
			self.run_motor(self._motorA, self._motorB, ROTATIONS_PER_CM * math.fabs(distance) - 20, "forward")
		else:
			self.run_motor(self._motorA, self._motorB, ROTATIONS_PER_CM * math.fabs(distance) - 20, "backward")

	def turn(self, degrees): #degrees in encoder degree
		index = self.direction(degrees)
		increase = 1
		if (degrees < 0):
			increase = 1.5 
		self._motorB.set_speed(-1 * index * TURN_SPEED * increase)
		self._motorA.set_speed(index * TURN_SPEED)
		self.run_motor(self._motorA, self._motorB, ROTATIONS_PER_DEGREE * math.fabs(degrees) - 10, "turn")		

	def run_motor(self, reference_motor, other_motor, degrees_to_turn, movement):
		self.error = 0
		BrickPiUpdateValues()
		initial_rotation = reference_motor.update_and_return_initial_rotation()
		initial_rotation_other = other_motor.update_and_return_initial_rotation()
		other_motor.set_initial_rotation()
		reference_motor.set_start_rotation()
		other_motor.set_start_rotation()
		self.initial_time = time.time()
		init_time = self.initial_time
		last_rotation = reference_motor.get_current_rotation()
		temp = 0
		while (math.fabs(reference_motor.get_current_rotation() - initial_rotation) < degrees_to_turn):
			curr_rotation = reference_motor.get_current_rotation()
			rotations = curr_rotation - last_rotation
			self.update_particles(rotations, movement)
			temp += 1
			last_rotation = curr_rotation
			self.draw_particles()
			if (time.time() - init_time > 0.2):
				self.adjust_speed(reference_motor, other_motor, self.initial_time, movement)
			curr_time = time.time()
			BrickPiUpdateValues()
		self._motorA.set_speed(0)
		self._motorB.set_speed(0)
		BrickPiUpdateValues()
		rotations = reference_motor.get_current_rotation() - last_rotation 
		self.update_particles(rotations, movement)
		self.draw_particles()
		#print("turned_total ", (reference_motor.get_current_rotation() - initial_rotation)/ROTATIONS_PER_DEGREE)
		#print("turned_degrees last", reference_motor.get_current_rotation() - initial_rotation)
		curr_time = time.time()
		count = 0
	
	def draw_particles(self):
		print "drawParticles:" + str(map(self.particle_to_tuple, self._particles))

	def update_particles(self, rotations, movement):
		if movement == "forward" or movement == "backward":
			distance_moved = (rotations)/ROTATIONS_PER_CM
			self.move_forward(distance_moved)
		if movement == "turn":
			degree_moved = (rotations)/ROTATIONS_PER_DEGREE
			self.move_turn(degree_moved)

	def move_forward(self, distance_moved):
		for particle in self._particles:
			particle.update_distance(distance_moved)

	def move_turn(self, degree_moved):
		for particle in self._particles:
			particle.update_rotation(degree_moved)

	def particle_to_tuple(self, particle):
		return particle.draw()

	def get_current_position(self):
		x_mean = 0
		y_mean = 0
		theta_mean = 0
		for p in self._particles:
			x_mean += p.get_x() * p.get_weight()
			y_mean += p.get_y() * p.get_weight()
			theta_mean += p.get_theta() * p.get_weight()
		return (x_mean, y_mean, theta_mean)

	def navigateToWaypoint(self, x, y):
		BrickPiUpdateValues()
		initial_rotation = self._motorA.get_current_rotation()
		(x_curr, y_curr, theta_curr) = self.get_current_position()
		theta = self.get_degrees_to_turn(x_curr, y_curr, theta_curr, x, y)
		print("theta!: ", theta)
		self.turn(theta)
		time.sleep(1)
		distance = self.get_distance_to_move(x_curr, y_curr, x, y)
		self.forward(distance)
		time.sleep(1)

	def get_distance_to_move(self, x_curr, y_curr, x, y):
		return math.sqrt(math.pow(x_curr - x, 2) + math.pow(y_curr - y, 2))
	
	def get_degrees_to_turn(self, x_curr, y_curr, theta_curr, x, y):
		theta_origin = math.degrees(math.atan2(y - y_curr, x - x_curr))
		print("theta_origin", theta_origin, "theta_curr", theta_curr)
		theta = (theta_origin - theta_curr) % 360
		print("theta without magic", theta)
		if(theta > 180):
			theta = theta - 360
		else:
			theta = theta	
		return theta

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
