# Jaikrishna # Initial Date: June 24, 2013 # Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

import math

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_A] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1     #Enable the Motor A
ROTATIONS_PER_CM = 29.85
ROTATIONS_PER_DEGREE = 10/9
FORWARD_SPEED_A = 100
FORWARD_SPEED_B = 100
TURN_SPEED = 100
K_p_f = 0.01
K_i_f = 0.05
K_d_f = 0.0001

K_p_t = 0.18
K_i_t = 0.1
K_d_t = 0.01



TIME_DIFF = 0.001


ERROR = 0

BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

def forward(distance_cm):
	BrickPiUpdateValues() 
	curr_degree = BrickPi.Encoder[PORT_A]
	BrickPi.MotorSpeed[PORT_A] = FORWARD_SPEED_A   
	BrickPi.MotorSpeed[PORT_B] = FORWARD_SPEED_B    
	t = time.time()
	t_s = t
	rotations_A = BrickPi.Encoder[PORT_A] 
	rotations_B = BrickPi.Encoder[PORT_B] 
	s_rotations_A = rotations_A
	s_rotations_B = rotations_B
	while (BrickPi.Encoder[PORT_A] - curr_degree < ROTATIONS_PER_CM * distance_cm):
		t_diff = time.time() - t
		n_rotations_A = BrickPi.Encoder[PORT_A] 
		n_rotations_B = BrickPi.Encoder[PORT_B] 
		if((time.time() - t_s) > 0.1 and t_diff > TIME_DIFF):
			speed_A = (n_rotations_A - rotations_A)/t_diff
			speed_B = (n_rotations_B - rotations_B)/t_diff
			adjustment = control(speed_A, speed_B, s_rotations_A, s_rotations_B, n_rotations_A, n_rotations_B, t_diff, K_p_f, K_i_f, K_d_f)
			print (int(adjustment))
			BrickPi.MotorSpeed[PORT_B] += int(adjustment)
			t = time.time()
			rotations_A = n_rotations_A
			rotations_B = n_rotations_B
			BrickPiUpdateValues() 

def turn(degrees):
	BrickPiUpdateValues() 
	BrickPi.MotorSpeed[PORT_A] = TURN_SPEED   
	BrickPi.MotorSpeed[PORT_B] = -1*TURN_SPEED    
	if(degrees < 0):
		BrickPi.MotorSpeed[PORT_A] = -1*TURN_SPEED   
		BrickPi.MotorSpeed[PORT_B] = TURN_SPEED    
	curr_degree = BrickPi.Encoder[PORT_A]
	t = time.time()
	rotations_A = BrickPi.Encoder[PORT_A] 
	rotations_B = BrickPi.Encoder[PORT_B] 
	s_rotations_A = rotations_A
	s_rotations_B = rotations_B
	while (BrickPi.Encoder[PORT_A] - curr_degree < 100):
		t_diff = time.time() - t
		n_rotations_A = BrickPi.Encoder[PORT_A] 
		n_rotations_B = BrickPi.Encoder[PORT_B] 
		if(t_diff > TIME_DIFF):
			speed_A = math.fabs(n_rotations_A - rotations_A)/t_diff
			speed_B = math.fabs(n_rotations_B - rotations_B)/t_diff
			adjustment = control(speed_A, speed_B, s_rotations_A, s_rotations_B, n_rotations_A, n_rotations_B, t_diff, K_p_t, K_i_t, K_d_t)
			print (int(adjustment))
			BrickPi.MotorSpeed[PORT_B] -= int(adjustment)
			t = time.time()
			rotations_A = n_rotations_A
			rotations_B = n_rotations_B
			BrickPiUpdateValues() 



def control(speed_A, speed_B, s_rotations_A, s_rotations_B, n_rotations_A, n_rotations_B, t_diff, K_p, K_i, K_d):
	global ERROR
	error = speed_A - speed_B
	derivative = (error - ERROR)/t_diff
	integral = math.fabs(n_rotations_A - s_rotations_A) - math.fabs(n_rotations_B - s_rotations_B) 
	out = K_p * error + K_i*integral + K_d * derivative
	print("out: " , out , ", error: " , error , " ,integral: " , integral, " , derivative:" , derivative)
	ERROR = error
	return out

forward(80)
#time.sleep(1.0)
#turn(90)
'''
for i in range(0,4):
	forward(40)
	time.sleep(1.5)
	turn(90)
	time.sleep(1.5)
'''
