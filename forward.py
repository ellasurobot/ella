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

DISTANCE = 40		# move forward in cm
END_POINT = DISTANCE * 10 + 50

line1 = (50, 50, 50, END_POINT) # (x0, y0, x1, y1)
line2 = (50, 50, END_POINT, 50)  # (x0, y0, x1, y1)
line3 = (50, END_POINT, END_POINT, END_POINT) # (x0, y0, x1, y1)
line4 = (END_POINT, 50, END_POINT, END_POINT) # (x0, y0, x1, y1)

print "drawLine:" + str(line1)
print "drawLine:" + str(line2)
print "drawLine:" + str(line3)
print "drawLine:" + str(line4)
robot.forward(DISTANCE)
