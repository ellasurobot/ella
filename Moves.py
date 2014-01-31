from BrickPi import *   #import BrickPi.py file to use BrickPi operations

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

