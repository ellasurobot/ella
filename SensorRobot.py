from Motor import *
from MotorSettings import*
from RobotSettings import *
import math

class SensorRobot(Robot):

    def __init__(self):
        BrickPiSetup()  # setup the serial port for communication
        
        self.__motorA = Motor("PORT_A") 
        self.__motorB = Motor("PORT_B")
        self.__left_touch = Sensor("PORT_1", "touch")
        self.__right_touch = Sensor("PORT_2", "touch")
        self.__sonar = Sensor("PORT_3", "sonar")


        BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

    def forward(self, bump_distance = 0):
        index = 1
	self.__motorA.set_speed(index * FORWARD_SPEED_A)
        self.__motorB.set_speed(index * FORWARD_SPEED_B)
        while(True):
            left_bumped = self.__left_touch.get_value()
            right_bumped = self.__right_touch.get_value()
            if (left_bumped and right_bumped):
                super(SensorRobot,self).forward(-10)
                super(SensorRobot,self).turn(90)
                
