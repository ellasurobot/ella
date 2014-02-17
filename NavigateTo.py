from Robot import *
from DrawSquare import *

robot = Robot()
#draw_square(40)
draw_assignment()

#robot.navigateToWaypoint(40, 0)
#robot.navigateToWaypoint(40, 40)
#robot.navigateToWaypoint(0, 40)
#robot.navigateToWaypoint(0, 0)

robot.navigateToWaypoint(50, 50)
robot.navigateToWaypoint(50, -20)
robot.navigateToWaypoint(0, 0)
