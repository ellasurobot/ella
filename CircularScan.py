from RobotNav import *
import sys
import random
import math
from place_rec_bits import *
from particleDataStructures import Map, Canvas

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


robot = RobotNav(wall_map, canvas)
#robot.turn_sonar(90)

#print "drawParticles:" + str([(,0,0)] )

centre = (400,400)

robot.turn_sonar(360)

