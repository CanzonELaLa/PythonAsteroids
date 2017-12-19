class Asteroid:
    def __init__(self, location, velocity, size):
        self.__position_x = location[0]
        self.__position_y = location[1]
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]
        self.__size = size

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

    def get_size(self):
        return self.__size

    def move(self):
        pass