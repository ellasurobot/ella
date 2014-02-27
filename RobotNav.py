from Robot import *
from Sensor import *
from place_rec_bits import *

MOTOR_SONAR_SPEED = 50
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
			for degree in range(len(ls.sig)):
#				self.turn_sonar(1)
	# reading = random.randint(0,255)
				BrickPiUpdateValues()
				reading = self.get_sonar_value()
				ls.sig[degree] = reading
				x = CENTRE_SCREEN[0] + reading * math.cos(math.radians(degree))
				y = CENTRE_SCREEN[1] + reading * math.sin(math.radians(degree))
				print "drawLine:" + str(CENTRE_SCREEN + (x,y))

	# FILL IN: compare two signatures
	def compare_signatures(self, ls1, ls2):
			dist = 0
			print "TODO:    You should implement the function that compares two signatures."
			return dist

	# This function characterizes the current location, and stores the obtained 
	# signature into the next available file.
	def learn_location(self):
			ls = LocationSignature()
			self.characterize_location(ls)
			idx = self._signatures.get_free_index();
			if (idx == -1): # run out of signature files
					print "\nWARNING:"
					print "No signature file is available. NOTHING NEW will be learned and stored."
					print "Please remove some loc_%%.dat files.\n"
					return
			
			self._signatures.save(ls,idx)
			print "STATUS:  Location " + str(idx) + " learned and saved."

	# This function tries to recognize the current location.
	# 1.   Characterize current location
	# 2.   For every learned locations
	# 2.1. Read signature of learned location from file
	# 2.2. Compare signature to signature coming from actual characterization
	# 3.   Retain the learned location whose minimum distance with
	#      actual characterization is the smallest.
	# 4.   Display the index of the recognized location on the screen
	def recognize_location(self):
			ls_obs = LocationSignature();
			self.characterize_location(ls_obs);

			# FILL IN: COMPARE ls_read with ls_obs and find the best match
			for idx in range(self._signatures.size):
					print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
					ls_read = self._signatures.read(idx);
					dist    = self.compare_signatures(ls_obs, ls_read)



