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
    #
    # def move(self):
    #     new_vel_x = self.__velocity_x + self.ACCELERATION_COEFFICIANT * cos(
    #         self.__rad_heading)
    #     new_vel_y = self.__velocity_y + self.ACCELERATION_COEFFICIANT * sin(
    #         self.__rad_heading)
    #     self.set_velocity([new_vel_x, new_vel_y])