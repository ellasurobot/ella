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
ROTATIONS_PER_CM = 23.25
ROTATIONS_PER_DEGREE = 13/9
FORWARD_SPEED_A = 232
FORWARD_SPEED_B = 200
TURN_SPEED = 150


BrickPiSetupSensors()       #Send the properties of sensors to BrickPi


for i in range(0,4):
	forward(40)
	time.sleep(1.5)
	turn(90)
	time.sleep(1.5)
