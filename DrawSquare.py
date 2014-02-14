OFFSET = 200
ZOOM_FACTOR = 10


def draw_square(distance):
	END_POINT = distance * ZOOM_FACTOR + OFFSET 

	line1 = (OFFSET, OFFSET, OFFSET, END_POINT) 
	line2 = (OFFSET, OFFSET, END_POINT, OFFSET)  
	line3 = (OFFSET, END_POINT, END_POINT, END_POINT) 
	line4 = (END_POINT, OFFSET, END_POINT, END_POINT) 

	print "drawLine:" + str(line1)
	print "drawLine:" + str(line2)
	print "drawLine:" + str(line3)
	print "drawLine:" + str(line4)

def draw_assignment():

	x_1 = OFFSET 
	y_1 = 50 * ZOOM_FACTOR + OFFSET
	x_2 = 50 * ZOOM_FACTOR + OFFSET
	y_2 = OFFSET
	x_3 = 50 * ZOOM_FACTOR + OFFSET
	y_3 = 70 * ZOOM_FACTOR + OFFSET 
			

	line1 = (x_1, y_1, x_2, y_2)
	line2 = (x_2, y_2, x_3, y_3)
	line3 = (x_3, y_3, x_1, y_1)

	print "drawLine:" + str(line1)
	print "drawLine:" + str(line2)
	print "drawLine:" + str(line3)
