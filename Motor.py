from BrickPi import *

class Motor:
	def __init__(self, port):
		self.__port = port
		BrickPi.MotorEnable[__port] = 1     #Enable the Motor

	def get_speed():
		return BrickPi.MotorSpeed[self.__port]

	def set_speed(speed):
		BrickPi.MotorSpeed[self.__port] = speed
		    
	def get_current_rotation():
		return BrickPi.Encoder[self.__port]

