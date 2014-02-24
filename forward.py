# Jaikrishna # Initial Date: June 24, 2013 # Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

#from Moves import forward, turn
from Robot import *
from DrawSquare import *
import sys

robot = Robot()

DISTANCE = int(sys.argv[1])		# move forward in cm
draw_square(DISTANCE)
#robot.forward(DISTANCE)
for i in range(7):
	robot.forward(15)
	time.sleep(0.5)
