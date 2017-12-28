###############################################################
# Imports
###############################################################

from math import sin, cos, radians
from vector import Vector

###############################################################
# Class definition
###############################################################


class Ship:
    """
    Describes a ship's location, velocity and heading
    """

    RADIUS = 1
    INITIAL_HEADING = 0
    INITIAL_SHIP_LIVES = 3

    def __init__(self, location, velocity=Vector(0, 0),
                 heading=INITIAL_HEADING):
        """ Initiates the class """
        self.__location = location  # Vector type
        self.__velocity = velocity  # Vector type
        self.__heading = heading
        self.__lives = self.INITIAL_SHIP_LIVES

    def get_lives(self):
        """
        gets ship lives
        """
        return self.__lives

    def subtract_life(self):
        """
        subtracts 1 life from ship
        """
        self.__lives -= 1

    def get_radius(self):
        """
        returns ship radius
        """
        return self.RADIUS

    def get_rad_heading(self):
        """
        returns ship heading in radians
        """
        return radians(self.__heading)

    def accelerate(self):
        """
        accelerates ship velocity in its heading
        """
        rad_heading = self.get_rad_heading()
        acceleration_vector = Vector(cos(rad_heading), sin(rad_heading))

        self.__velocity += acceleration_vector

    def rotate(self, increment):
        """
        :param increment: increment in degrees to change ship heading
        changes ship heading by provided increment.
        """
        self.__heading += increment

    def set_location(self, location):
        """
        :param location: location to place ship in
        sets ship's location
        """
        self.__location = location

    def get_location(self):
        """
        gets ship location
        """
        return self.__location

    def get_velocity(self):
        """
        gets ship velocity
        """
        return self.__velocity

    def get_heading(self):
        """
        gets ship heading
        """
        return self.__heading
