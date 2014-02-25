from BrickPi import *

class Motor:
	def __init__(self, port):
		port_dictionary = {
						"PORT_A":PORT_A,
						"PORT_B":PORT_B,
						"PORT_C":PORT_C
						}
		port_number = port_dictionary[port]
		self.__port = port_number
		BrickPi.MotorEnable[port_number] = 1     #Enable the Motor

	def get_speed(self):
		return BrickPi.MotorSpeed[self.__port]

	def set_speed(self, speed):
		BrickPi.MotorSpeed[self.__port] = int(speed)
		    
	def get_current_rotation(self):
		return BrickPi.Encoder[self.__port]

	def update_and_return_initial_rotation(self):
		self.set_initial_rotation() 
		return self.get_initial_rotation()

	def get_initial_rotation(self):
		return self.__initial_rotation

	def set_initial_rotation(self):
		self.__initial_rotation = self.get_current_rotation()

	def set_start_rotation(self):
		self.__start_rotation = self.get_current_rotation()

	def get_start_rotation(self):
		return self.__start_rotation
