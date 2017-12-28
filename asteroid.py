###############################################################
# Class definition
###############################################################


class Asteroid:
    """
    Describes an asteroid's location, velocity and size
    """

    RADIUS_MULTIPLIER = 10
    RADIUS_NORMALIZATION_FACTOR = -5

    BIG_ASTEROID_SIZE = 3
    BIG_ASTEROID_SCORE = 20

    MEDIUM_ASTEROID_SIZE = 2
    MEDIUM_ASTEROID_SCORE = 50

    SMALL_ASTEROID_SIZE = 1
    SMALL_ASTEROID_SCORE = 100

    def __init__(self, location, velocity, size):
        """ Initiates the class """
        self.__location = location  # Vector type
        self.__velocity = velocity  # Vector type
        self.__size = size

    def get_radius(self):
        """
        calculates asteroid radius.
        """
        return self.__size * self.RADIUS_MULTIPLIER + \
               self.RADIUS_NORMALIZATION_FACTOR

    def get_location(self):
        """
        gets asteroid location.
        """
        return self.__location

    def set_location(self, location):
        """
        :param location: Vector in which to place asteroid
        sets asteroid location to location.
        """
        self.__location = location

    def get_velocity(self):
        """
        gets asteroid velocity.
        """
        return self.__velocity

    def get_size(self):
        """
        gets asteroid size
        """
        return self.__size

    def has_intersection(self, obj):
        """
        :param obj: object to check if asteroid intersects with
        :return: True of asteroid and obj are intersecting and False otherwise.
        Returns True if the distance between the locations of the objects
         is less than or equal to their combined radii.
        """
        if self.__location.get_distance(obj.get_location())\
                <= (self.get_radius() + obj.get_radius()):
            return True
        return False

    def get_score(self):
        """
        gets asteroid score worth by asteroid size
        """
        if self.__size == self.BIG_ASTEROID_SIZE:
            return self.BIG_ASTEROID_SCORE
        elif self.__size == self.MEDIUM_ASTEROID_SIZE:
            return self.MEDIUM_ASTEROID_SCORE
        elif self.__size == self.SMALL_ASTEROID_SIZE:
            return self.SMALL_ASTEROID_SCORE
