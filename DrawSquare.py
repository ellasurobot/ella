ORIGIN_X = 200
ORIGIN_Y = 600
ZOOM_FACTOR = 7


def draw_square(distance):
	(x_1, y_1) = display(0, 0)
	(x_2, y_2) = display(0, 40)
	(x_3, y_3) = display(40, 40)
	(x_4, y_4) = display(40, 0)

	line1 = (x_1, y_1, x_2, y_2)
	line2 = (x_2, y_2, x_3, y_3)
	line3 = (x_3, y_3, x_4, y_4)
	line4 = (x_4, y_4, x_1, y_1)

	print "drawLine:" + str(line1)
	print "drawLine:" + str(line2)
	print "drawLine:" + str(line3)
	print "drawLine:" + str(line4)

def draw_assignment():

	(x_1, y_1) = display(0, 0)
	(x_2, y_2) = display(50, 50)
	(x_3, y_3) = display(50, -20)

	line1 = (x_1, y_1, x_2, y_2)
	line2 = (x_2, y_2, x_3, y_3)
	line3 = (x_3, y_3, x_1, y_1)

	print "drawLine:" + str(line1)
	print "drawLine:" + str(line2)
	print "drawLine:" + str(line3)

def display(x, y):
	new_x = ORIGIN_X + x * ZOOM_FACTOR
	new_y = ORIGIN_Y - y * ZOOM_FACTOR 
	return (new_x, new_y)
	
