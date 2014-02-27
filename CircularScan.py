from RobotNav import *
import sys
import random
import math

robot = RobotNav()
#robot.turn_sonar(90)

#print "drawParticles:" + str([(,0,0)] )

centre = (400,400)

for degree in range(360):
	robot.turn_sonor(1)
#	reading = random.randint(0,255)
	reading = robot.get_sonar_value()
	x = centre[0] + reading * math.cos(math.radians(degree))
	y = centre[1] + reading * math.sin(math.radians(degree))
	print "drawLine:" + str(centre + (x,y))
	

