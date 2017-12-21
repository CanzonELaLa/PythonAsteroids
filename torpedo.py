from math import sin, cos, radians


class Torpedo:
    RADIUS = 4
    ACCELERATION_COEFFICIANT = 2

    def __init__(self, location, velocity, heading):
        self.__position_x = location[0]
        self.__position_y = location[1]
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]
        self.__heading = heading
        self.__rad_heading = radians(heading)
        self.__radius = self.RADIUS
        self.__life_time = 0

    def get_radius(self):
        return self.__radius

    def set_location(self, location):
        self.__position_x = location[0]
        self.__position_y = location[1]

    def set_position_x(self, x):
        self.__position_x = x

    def set_position_y(self, y):
        self.__position_y = y

    def get_position_x(self):
        return self.__position_x

    def get_position_y(self):
        return self.__position_y

    def get_location(self):
        return [self.__position_x, self.__position_y]

    def set_velocity(self, velocity):
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]

    def get_velocity_x(self):
        return self.__velocity_x

    def get_velocity_y(self):
        return self.__velocity_y

    def get_velocity(self):
        return [self.__velocity_x, self.__velocity_y]

    def get_heading(self):
        return self.__heading

    def add_life_time(self):
        self.__life_time += 1

    def get_life_time(self):
        return self.__life_time