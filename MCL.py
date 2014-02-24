from RobotMCL import *
from particleDataStructures import Map, Canvas
import globals

canvas = Canvas()
wall_map = Map(canvas)
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
wall_map.add_wall((0,0,0,168));        # a
wall_map.add_wall((0,168,84,168));     # b
wall_map.add_wall((84,126,84,210));    # c
wall_map.add_wall((84,210,168,210));   # d
wall_map.add_wall((168,210,168,84));   # e
wall_map.add_wall((168,84,210,84));    # f
wall_map.add_wall((210,84,210,0));     # g
wall_map.add_wall((210,0,0,0));        # h
wall_map.draw();


print("point 1!")
robot = RobotMCL(wall_map, 84, 30, canvas)
print("point 2!")
robot.navigate_to_way_point_a_bit(180, 30)

print("point 3!")
robot.navigate_to_way_point_a_bit(180, 54)
print("point 4!")
robot.navigate_to_way_point_a_bit(126, 54)

robot.navigate_to_way_point_a_bit(126, 126)
print("point 5!")
robot.navigate_to_way_point_a_bit(126, 168)

#robot = RobotMCL(wall_map, 126, 168, canvas)
print("point 6!")
robot.navigate_to_way_point_a_bit(126, 126)
#robot.navigate_to_way_point_a_bit(130, 126)
#globals.BIG_ANGLE = True
#globals.BAD = True
print("point 7!")
globals.VAR_BIG = True
robot.navigate_to_way_point_a_bit(34, 65)
globals.BAD = False
globals.VAR_BIG = False
robot.navigate_to_way_point_a_bit(30, 54)

print("point 8!")
robot.navigate_to_way_point_a_bit(84, 54)
print("point 9!")
robot.navigate_to_way_point_a_bit(84, 30)
