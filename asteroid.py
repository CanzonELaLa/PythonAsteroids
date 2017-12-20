class Asteroid:

    RADIUS_MULT = 10
    RADIUS_MINUS = -5

    def __init__(self, location, velocity, size):
        self.__position_x = location[0]
        self.__position_y = location[1]
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]
        self.__size = size
        self.__radius = self.get_radius()

    def get_radius(self):
        return self.__size * self.RADIUS_MULT + self.RADIUS_MINUS

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

    def has_intersection(self, obj):
        if self.distance(obj) <= self.get_radius() + obj.get_radius():
            return True
        return False

    def distance(self, obj):
        return ((self.__position_x - obj.position_x) ** 2 +
                (self.__position_y - obj.position_y) ** 2) ** 0.5