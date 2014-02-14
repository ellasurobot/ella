from Robot import *

robot = Robot()

DISTANCE = 40		# move forward in cm
END_POINT = DISTANCE * 10 + 100 

line1 = (100, 100, 100, END_POINT) # (x0, y0, x1, y1)
line2 = (100, 100, END_POINT, 100)  # (x0, y0, x1, y1)
line3 = (100, END_POINT, END_POINT, END_POINT) # (x0, y0, x1, y1)
line4 = (END_POINT, 100, END_POINT, END_POINT) # (x0, y0, x1, y1)

print "drawLine:" + str(line1)
print "drawLine:" + str(line2)
print "drawLine:" + str(line3)
print "drawLine:" + str(line4)

robot.navigateToWaypoint(0.0, DISTANCE)
