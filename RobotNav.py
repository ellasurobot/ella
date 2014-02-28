from Robot import *
from Sensor import *
from place_rec_bits import *
import sys

MOTOR_SONAR_SPEED = 120 
ROTATION_PER_DEGREE_SONAR = 1
CENTRE_SCREEN = (400,400)

class RobotNav(Robot):
	
	def __init__(self):
		Robot.__init__(self)
		self._motorSonar = Motor("PORT_C") 
		self._sonar = Sensor("PORT_2", "sonar")
		BrickPiSetupSensors()	
		self._signatures = SignatureContainer(5)

	def get_sonar_value(self):
		return self._sonar.get_value()	

	def turn_sonar(self, angle):
		index = angle/abs(angle)
		self._motorSonar.set_speed(index*MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		degrees_to_turn = abs(angle) * ROTATION_PER_DEGREE_SONAR
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()

		while (math.fabs(self._motorSonar.get_current_rotation() - initial_rotation) < degrees_to_turn):
			#			if(
			BrickPiUpdateValues()
		self._motorSonar.set_speed(0)

	def scan_and_plot(self):
		for degree in range(360):
			#				self.turn_sonar(1)
			BrickPiUpdateValues()
			reading = self.get_sonar_value()
			x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
			y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
			print "drawLine:" + str(CENTRE_SCREEN + (x,y))

	# FILL IN: spin robot or sonar to capture a signature and store it in ls
	def characterize_location(self, ls):
		self._motorSonar.set_speed(MOTOR_SONAR_SPEED)
		BrickPiUpdateValues()
		initial_rotation = self._motorSonar.update_and_return_initial_rotation()
		last_rotation = self._motorSonar.get_current_rotation()
		degree = 0
		while (math.fabs(self._motorSonar.get_current_rotation() - initial_rotation) < 360*ROTATION_PER_DEGREE_SONAR):
			if(self._motorSonar.get_current_rotation() - last_rotation > ROTATION_PER_DEGREE_SONAR):
				reading = self.get_sonar_value()
				ls.sig[degree] = reading
				x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
				y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
				print "drawLine:" + str(CENTRE_SCREEN + (x,y))
				last_rotation = self._motorSonar.get_current_rotation()
				degree += 1 
			BrickPiUpdateValues()
		self._motorSonar.set_speed(0)

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
		self.characterize_location(obs_signatre)
	 	saved_signatures = [self._signatures.read(idx) for idx in range(self._signatures.size)]
		self.find_best_fit(obs_signature, saved_signatures)

	def recognize_location_for_any_rotation(self):
		signature = HistogramSignature()
		self.characterize_location(signature)
		signature.calculate_histogram()
	 	saved_signatures = [self._signatures.read(idx) for idx in range(self._signatures.size)]
		self.find_best_fit(signature, saved_signatures)

	# This function tries to recognize the current location.
	# 1.   Characterize current location
	# 2.   For every learned locations
	# 2.1. Read signature of learned location from file
	# 2.2. Compare signature to signature coming from actual characterization
	# 3.   Retain the learned location whose minimum distance with
	#      actual characterization is the smallest.
	# 4.   Display the index of the recognized location on the screen
	def find_best_fit(self, obs_sign, saved_signs):
		ls_obs = LocationSignature();
		self.characterize_location(ls_obs);
		# FILL IN: COMPARE ls_read with ls_obs and find the best match
		index_best_fit = -1
		min_sq_diff = sys.maxint
		idx = 0
		for sign in saved_signs:
			print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
			sq_diff = self.sum_of_squares(obs_sign.get_data(), sign.get_data())
			if sq_diff < min_sq_diff:	
				min_sq_diff = sq_diff
				index_best_fit = idx	
			idx += 1 
		print("Best fit for location: ", idx, ", with sq_diff: ", min_sq_diff)


