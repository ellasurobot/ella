from BrickPi import *

class Sensor:
    def __init__(self, port, sensor_type):
        	port_dictionary = {
                    "PORT_1":PORT_1,
                    "PORT_2":PORT_2,
                    "PORT_3":PORT_3,
										"PORT_4":PORT_4
                    }
                type_dictionary = {
                    "touch":TYPE_SENSOR_TOUCH,
                    "sonar":TYPE_SENSOR_ULTRASONIC_CONT
                    }
                port_number = port_dictionary[port]
                self.__port = port_number
                s_type = type_dictionary[sensor_type]
                BrickPi.SensorType[port_number] = s_type

    def get_value(self):
        return BrickPi.Sensor[self.__port]
