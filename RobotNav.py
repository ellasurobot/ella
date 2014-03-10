from RobotMCL import *
from Sensor import *
from place_rec_bits import *
import sys
import time
import collections
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)    #GPIO 18
GPIO.setup(13, GPIO.OUT)    #GPIO 27

DIFF_TRESHOLD = 3
MOTOR_SONAR_SPEED = 60
ROTATION_PER_DEGREE_SONAR = 3 
CENTRE_SCREEN = (400,400)

point_index_map = {0:1, 1:2, 2:4, 3:5, 4:7}
points = {1: (84, 30), 
				 	2: (180, 30), 
					4: (126, 54), 
					5: (126, 168), 
					7: (30, 54)}

class RobotNav(RobotMCL):
	
	def __init__(self, wall_map=None, canvas=None):
		RobotMCL.__init__(self, wall_map, 0, 0, canvas)
		self._particles = [ParticleMCL(0, 0, 0, (1.0/NUMBER_OF_PARTICLES), self._map) for i in range(NUMBER_OF_PARTICLES)]	
		self._motorSonar = Motor("PORT_C") 
		self._sonar = Sensor("PORT_4", "sonar")
		BrickPiSetupSensors()	
		self._signatures = SignatureContainer(5)
		self.computed_histogram = self.create_histograms()

	def create_histograms(self):
		histograms = []
		for i in range(0,5):
			print("array ", i)
			(x, y) = points[point_index_map[i]]		
			histogram = []
			for j in range(0, 360):
				(m, wall) = self.calc_min_distance_to_wall(x, y, j)
				histogram.append(m)		
			#print histogram
			histograms.append(histogram)
		return histograms

	def calc_min_distance_to_wall(self, x, y, j):
		ms = self.calc_distances_to_walls(x,y,j)
		for (m, wall) in ms:
			if self.in_wall_of(m, x, y, j, wall):
				return (m, wall)
		return (sys.maxint, wall)

	def calc_distances_to_walls(self, x, y, j):
		return sorted([self.calculate_m(x, y, j, wall) for wall in self.get_wall_map()])
	
	def calculate_m(self, x, y,	j, (Ax, Ay, Bx, By)):
		theta = j
		top = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
		bottom = (By - Ay) * math.cos(math.radians(theta)) - (Bx - Ax) * math.sin(math.radians(theta))
		if (bottom == 0) or (top/bottom) < 0:
			return (sys.maxint, (Ax, Ay, Bx, By))
		else:
			return (top / bottom, (Ax, Ay, Bx, By))    

	def in_wall_of(self, m, x, y, j, (x1, y1, x2, y2)):
		theta = j
		x += math.cos(math.radians(theta)) * m
		y += math.sin(math.radians(theta)) * m
		return (min(x1, x2) <= round(x) <= max(x1, x2) and min(y1, y2) <= round(y) <= max(y1, y2))
	

	def update_location(self, x, y, theta):
		self._particles = [ParticleMCL(x, y, theta, (1.0/NUMBER_OF_PARTICLES), self._map) for i in range(NUMBER_OF_PARTICLES)]	

	def get_sonar_value(self):
		return self._sonar.get_value()	

	def turn_sonar(self, angle):
		index = angle/abs(angle)
		self._motorSonar.set_speed(index*MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		degrees_to_turn = abs(angle) * ROTATION_PER_DEGREE_SONAR
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()
		curr_rotation = initial_rotation
		while (math.fabs(self._motorSonar.get_current_rotation() - initial_rotation) < degrees_to_turn):
			rotation = self._motorSonar.get_current_rotation()
			if(True):
				curr_rotation = rotation
				degree = (rotation - initial_rotation)/ROTATION_PER_DEGREE_SONAR
				reading = self.get_sonar_value()
				x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
				y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
				print "drawLine:" + str(CENTRE_SCREEN + (x,y))
				print("degree turned: ", degree, "sonar reading: ", reading)
			BrickPiUpdateValues()
		print("rotations done: ", self._motorSonar.get_current_rotation() - initial_rotation)
		self._motorSonar.set_speed(0)

	def scan_and_plot(self):
		self._motorSonar.set_speed(MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()
		last_rotation = self._motorSonar.get_current_rotation()
		degree = 0
		while (math.fabs(self._motorSonar.get_current_rotation() - initial_rotation) < 360*ROTATION_PER_DEGREE_SONAR):
			if(self._motorSonar.get_current_rotation() - last_rotation > ROTATION_PER_DEGREE_SONAR):
				reading = self.get_sonar_value()
				x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
				y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
				print "drawLine:" + str(CENTRE_SCREEN + (x,y))
				last_rotation = self._motorSonar.get_current_rotation()
				degree -= 1
			BrickPiUpdateValues()
		self._motorSonar.set_speed(0)
		BrickPiUpdateValues()

	# FILL IN: spin robot or sonar to capture a signature and store it in ls
	'''
	def characterize_location(self, ls):
		self._motorSonar.set_speed(MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()
		last_rotation = self._motorSonar.get_current_rotation()
		index = 0
		while (index < 360):
			degree_motor = math.fabs(self._motorSonar.get_current_rotation() - initial_rotation)
			if(degree_motor > (index+1) * ROTATION_PER_DEGREE_SONAR):
				degree = degree_motor / ROTATION_PER_DEGREE_SONAR
				reading = self.get_sonar_value()
				ls.sig[index] = reading
				index += 1
				x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
				y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
				print "drawLine:" + str(CENTRE_SCREEN + (x,y))
				last_rotation = self._motorSonar.get_current_rotation()
			BrickPiUpdateValues()
		self._motorSonar.set_speed(0)
		print("Readings: ", ls.sig, "with length: ", len(ls.sig))
		BrickPiUpdateValues()
'''
	def characterize_location(self, ls):
		self._motorSonar.set_speed(MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()
		degrees_to_turn = 360 * ROTATION_PER_DEGREE_SONAR
		index = 0
		curr_rotation = initial_rotation
		while (math.fabs(self._motorSonar.get_current_rotation() - initial_rotation) < degrees_to_turn):	
			rotation = self._motorSonar.get_current_rotation()
			degree = (rotation - initial_rotation)/ROTATION_PER_DEGREE_SONAR
			reading = self.get_sonar_value()
	#		x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
#			y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
#			print "drawLine:" + str(CENTRE_SCREEN + (x,y))
			ls.sig[int(degree)] = reading
			BrickPiUpdateValues()
		self._motorSonar.set_speed(0)
		ls.complete_sig()
		print("Readings: ", ls.sig, "with length: ", len(ls.sig))
		BrickPiUpdateValues()

	# FILL IN: compare two signatures
	def sum_of_squares(self, list1, list2):
		sq_diff = sum(map(lambda (x,y): math.pow(x-y,2),zip(list1, list2)))
		return sq_diff

	def learn_specific_location(self, idx):
		ls = LocationSignature()
		self.characterize_location(ls)
		self._signatures.save(ls,idx)
		print "STATUS:  Location " + str(idx) + " learned and saved."

	# Learns location i that is determined by the first loc_0i.dat that doesn't
	# exist yet.
	def learn_location(self):
		idx = self._signatures.get_free_index();
		if (idx == -1): # run out of signature files
			print "\nWARNING:"
			print "No signature file is available. NOTHING NEW will be learned and stored."
			print "Please remove some loc_%%.dat files.\n"
			return
		self.learn_specific_location(idx)	

	def recognize_location(self):
		obs_signature = LocationSignature()
		self.characterize_location(obs_signature)
	 	saved_signatures = [self._signatures.read(idx) for idx in range(self._signatures.size)]
		self.find_best_fit(obs_signature, saved_signatures)

	def try_to_recover(self, index, x, y, theta):
		BrickPiUpdateValues()
		time.sleep(0.5)
		assumed_sonar_reading = self.computed_histogram[index][theta]
		print("assumed_sonar_reading", assumed_sonar_reading)
		actual_sonar_reading = self.get_sonar_value()
		print("actual_sonar_reading", actual_sonar_reading)
		BrickPiUpdateValues()
		actual_sonar_reading = self.get_sonar_value()
		print("actual_sonar_reading", actual_sonar_reading)
		BrickPiUpdateValues()
		actual_sonar_reading = self.get_sonar_value()
		print("actual_sonar_reading", actual_sonar_reading)
		new_theta = theta
		if(math.fabs(actual_sonar_reading - assumed_sonar_reading) > DIFF_TRESHOLD and actual_sonar_reading < 255):
			new_theta = self.get_correct_angle(index, theta, actual_sonar_reading)		
		return new_theta

	def get_correct_angle(self, index, theta, sonar_read):
		ANGLE_ERROR = 50 
		histogram = self.computed_histogram[index]
		start_index = theta - ANGLE_ERROR
		end_index = theta + ANGLE_ERROR		
		new_theta = theta
		diff = sys.maxint
		for i in range (start_index, end_index + 1):
			temp_diff = math.fabs(histogram[i%360] - sonar_read)
			if(temp_diff < diff):
				diff = temp_diff
				new_theta = i%360		
		return new_theta

	def recognize_location_for_any_rotation(self):
		signature = HistogramSignature()
		self.characterize_location(signature)
		signature.calculate_histogram()
	 	saved_signatures = [HistogramSignature(self._signatures.read(idx)) for idx in range(self._signatures.size)]
		i = 0
		for saved_sign in saved_signatures:
			print("current histogram vs saved histogram ",i ,": ", zip(signature.get_data(), saved_sign.get_data()))
			i += 1
		index = self.find_best_fit(signature, saved_signatures)
		angle = self.find_angle(signature.sig, saved_signatures[index].sig)
		print("location is: ", index, "angle of:", angle)
		return (index, angle)

	def find_angle(self, obs_sign, matched_sign):
		angle = -1
		obs_q = collections.deque(obs_sign)
		min_sq_diff = sys.maxint
		for i in range(360):
			sq_diff = self.sum_of_squares(obs_q, matched_sign)
			obs_q.rotate(1)
#			print("angle: ", i, "queue", obs_q, "matched:", matched_sign)
			if(sq_diff < min_sq_diff):
				min_sq_diff = sq_diff
				angle = i
#			print("find_angle: ", i, "sq_diff: ", sq_diff)
		return angle

	# This function tries to recognize the current location.
	# 1.   Characterize current location
	# 2.   For every learned locations
	# 2.1. Read signature of learned location from file
	# 2.2. Compare signature to signature coming from actual characterization
	# 3.   Retain the learned location whose minimum distance with
	#      actual characterization is the smallest.
	# 4.   Display the index of the recognized location on the screen
	def find_best_fit(self, obs_sign, saved_signs):
		# FILL IN: COMPARE ls_read with ls_obs and find the best match
		index_best_fit = -1
		min_sq_diff = sys.maxint
		idx = 0
		for sign in saved_signs:
			print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
			sq_diff = self.sum_of_squares(obs_sign.get_data(), sign.get_data())
			print ("diff: ", sq_diff, "index: ", idx)
			if sq_diff < min_sq_diff:	
				min_sq_diff = sq_diff
				index_best_fit = idx	
			idx += 1 
		return index_best_fit
		print("Best fit for location: ", index_best_fit, ", with sq_diff: ", min_sq_diff)

	def navigate_through_rest(self, points_list):
		for point in points_list:
			print("travelling to:", point)
			self.flash_lights()
			self.navigate_to_way_point_a_bit(point[0], point[1])

	def flash_lights(self):
		GPIO.output(12, True)
		GPIO.output(13, False)
		time.sleep(0.5)
		GPIO.output(12, False)
		GPIO.output(13, True)
		time.sleep(0.5)
		GPIO.output(12, False)
		GPIO.output(13, False)
