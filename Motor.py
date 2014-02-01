from BrickPi import *

class Motor:
	def __init__(self, port):
		self.__port = port
		BrickPi.MotorEnable[__port] = 1     #Enable the Motor
		self.__initial_rotation = 0

	def get_speed():
		return BrickPi.MotorSpeed[self.__port]

	def set_speed(speed):
		BrickPi.MotorSpeed[self.__port] = speed
		    
	def get_current_rotation():
		return BrickPi.Encoder[self.__port]

	def get_initial_rotation():
		return self.__initial_rotation

	def set_initial_rotation():
		self.__initial_rotation = get_current_rotation()
