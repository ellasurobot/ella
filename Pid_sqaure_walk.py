# Jaikrishna # Initial Date: June 24, 2013 # Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_A] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1     #Enable the Motor A
ROTATIONS_PER_CM = 23.25
ROTATIONS_PER_DEGREE = 10/9
FORWARD_SPEED_A = 232
FORWARD_SPEED_B = 200
TURN_SPEED = 150
K_p = 0
K_i = 0
K_d = 0

BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

def forward(distance_cm):
	BrickPiUpdateValues() 
	curr_degree = BrickPi.Encoder[PORT_A]
	BrickPi.MotorSpeed[PORT_A] = FORWARD_SPEED_A   
	BrickPi.MotorSpeed[PORT_B] = FORWARD_SPEED_B    
	while (BrickPi.Encoder[PORT_A] - curr_degree < 980):
    		BrickPiUpdateValues() 

def turn(degrees):
	BrickPiUpdateValues() 
	BrickPi.MotorSpeed[PORT_A] = TURN_SPEED   
	BrickPi.MotorSpeed[PORT_B] = -1*TURN_SPEED    
	if(degrees < 0):
		BrickPi.MotorSpeed[PORT_A] = -1*TURN_SPEED   
		BrickPi.MotorSpeed[PORT_B] = TURN_SPEED    
	curr_degree = BrickPi.Encoder[PORT_A]
	
	while (BrickPi.Encoder[PORT_A] - curr_degree < 113):
#		print BrickPi.Encoder[PORT_A] - curr_degree , degrees * ROTATIONS_PER_DEGREE
		BrickPiUpdateValues() 

def error():
	desired = BrickPi.Encoder[PORT_A]	
	expected = BrickPi.Encoder[PORT_B]
	e = desired - expected
	return e

TOTAL_ERROR = 0
ERROR = 0

#proportional
def derivative(e1, e2):
	return e1 - e2

#proportional
def integral():
  return TOTAL_ERROR

def control():
	e = error()
	deriv = derivative(e, ERROR)
	TOTAL_ERROR += e
	integr = integral()
	out = K_p * error + K_i*integral + K_d * derivative

ot = time.time()
COUNTER = 0
while(time.time() - ot < 1):
	COUNTER = COUNTER + 1
#print COUNTER

'''
for i in range(0,4):
	forward(40)
	time.sleep(1.5)
	turn(90)
	time.sleep(1.5)
'''
