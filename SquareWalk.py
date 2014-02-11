# Jaikrishna # Initial Date: June 24, 2013 # Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

#from Moves import forward, turn
from Robot import *

robot = Robot()

SLEEP_TIME = 1.5	# sleep 1.5s between each move
DISTANCE = 40		# move forward in cm
DEGREES = 90	# turn to the right in degrees

line1 = (0, 0, 0, 500) # (x0, y0, x1, y1)
line2 = (0, 0, 500, 0)  # (x0, y0, x1, y1)

print "drawLine:" + str(line1)
print "drawLine:" + str(line2)

for i in range(0,4):
	robot.forward(DISTANCE)
	time.sleep(SLEEP_TIME)
	robot.turn(DEGREES)
	time.sleep(SLEEP_TIME)
