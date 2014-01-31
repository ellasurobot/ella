from Motor import *

class Robot:
	def __init__(self):
		BrickPiSetup()  # setup the serial port for communication

		self.__motorA = Motor(PORT_A) 
		self.__motorB = Motor(PORT_B) 

		BrickPiSetupSensors()       #Send the properties of sensors to BrickPi
		BrickPiUpdateValues() 

	def forward(distance):  # distance is in cm



