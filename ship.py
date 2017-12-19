from math import sin, cos, radians

class Ship:

    def __init__(self, location, velocity, heading):
        self.position_x = location[0]
        self.position_y = location[1]
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]
        self.heading = heading
        self.__rad_heading = radians(heading)

    def accelerate(self):
        new_velocity_x = self.__velocity_x + cos(self.__rad_heading)
        new_velocity_y = self.__velocity_y + sin(self.__rad_heading)
        self.set_velocity([new_velocity_x, new_velocity_y])

    def rotate(self, increment):
        self.__heading += increment
        self.__rad_heading = radians(self.__heading)

    def set_location(self, location):
        self.position_x = location[0]
        self.position_y = location[1]

    def set_position_x(self, x):
        self.position_x = x

    def set_position_y(self, y):
        self.position_y = y

    def get_position_x(self):
        return self.position_x

    def get_position_y(self):
        return self.position_y

    def get_location(self):
        return [self.position_x, self.position_y]

    def set_velocity(self, velocity):
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]

    def get_velocity_x(self):
        return self.__velocity_x

    def get_velocity_y(self):
        return self.__velocity_y

    def set_heading(self, heading):
        self.heading = heading
        self.__rad_heading = radians(self.heading)

    def get_heading(self):
        return self.heading

    def move(self):
        pass
