# Jaikrishna # Initial Date: June 24, 2013 # Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from Moves import *


BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_A] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1     #Enable the Motor A

BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

SLEEP_TIME = 1.5	# sleep 1.5s between each move
DISTANCE = 40		# move forward in cm
DEGREES = 90	# turn to the right in degrees

for i in range(0,4):
	forward(DISTANCE)
	time.sleep(SLEEP_TIME)
	turn_right(DEGREES)
	time.sleep(SLEEP_TIME)
