from RobotNav import *
import sys
import random
import math
from place_rec_bits import *

robot = RobotNav()
#robot.turn_sonar(90)

#print "drawParticles:" + str([(,0,0)] )

centre = (400,400)

robot.learn_specific_location(0)
