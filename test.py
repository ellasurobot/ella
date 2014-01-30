# Jaikrishna # Initial Date: June 24, 2013 # Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

BrickPiSetup()  # setup the serial port for communication

speed = 100
BrickPi.MotorEnable[PORT_A] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1     #Enable the Motor A
BrickPi.MotorSpeed[PORT_A] = 150   #Set the speed of MotorA (-255 to 255)
BrickPi.MotorSpeed[PORT_B] = 150    #Set the speed of MotorA (-255 to 255)


BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

ot = time.time()
while (time.time() - ot < 3):
    result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
'''
    if not result :                 # if updating values succeeded
        print ( BrickPi.Encoder[PORT_A] %720 ) /2 , BrickPi.Encoder[PORT_A]  # print the encoder degrees 
    time.sleep(.1)		#sleep for 100 ms

#motorRotateDegree([100, 100], [90, 90], [PORT_A, PORT_B])

# Note: One encoder value counts for 0.5 degrees. So 360 degrees = 720 enc. Hence, to get degress = (enc%720)/2
'''
