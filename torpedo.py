###############################################################
# Imports
###############################################################

from math import radians

###############################################################
# Class definition
###############################################################


class Torpedo:
    """
    Describes a torpedo's location, velocity and heading
    """

    RADIUS = 4

    def __init__(self, location, velocity, heading):
        """ Initiates the class """
        self.__location = location
        self.__velocity = velocity
        self.__heading = heading
        self.__life_cycle = 0

    def get_radius(self):
        """
        gets torpedo radius
        """
        return self.RADIUS

    def get_location(self):
        """
        gets torpedo location
        """
        return self.__location

    def set_location(self, location):
        """
        :param location: location to place torpedo in
        sets torpedo location
        """
        self.__location = location

    def get_velocity(self):
        """
        gets torpedo velocity
        """
        return self.__velocity

    def get_heading(self):
        """
        gets torpedo heading
        """
        return self.__heading

    def add_life_cycle(self):
        self.__life_cycle += 1

    def get_life_cycle(self):
        return self.__life_cycle
