###############################################################
# Class definition
###############################################################


class Vector:

    def __init__(self, x, y):
        """ Initiates the class """
        self.__x = x
        self.__y = y

    def get_x(self):
        """
        returns x
        """
        return self.__x

    def get_y(self):
        """
        returns y
        """
        return self.__y

    def get_size(self):
        """
        calculates vector size
        """
        return (self.__x ** 2 + self.__y ** 2) ** 0.5

    def get_copy(self):
        """
        copies vector
        """
        return Vector(self.__x, self.__y)

    def __add__(self, other):
        """
        :param other: other vector to add to self
        :return: new vector which is has the sum of x and sum of y
        adds 2 vectors together to create a new vector
        """
        return Vector(self.__x + other.get_x(), self.__y + other.get_y())

    def __iadd__(self, other):
        """
        :param other: other vector to increment to current vector
        :return: self after being incremented with other
        adds the x value of other to self's and y value of other to self's.
        """
        self.__x += other.get_x()
        self.__y += other.get_y()
        return self

    def __sub__(self, other):
        """
        :param other: other vector to subtract from self
        :return: new vector which is has the difference of x and difference
        of y.
        Subtracts other from self to create a new vector.
        """
        return Vector(self.__x - other.get_x(), self.__y - other.get_y())

    def __mod__(self, other):
        """
        :param other: vector to modulate from self
        :return: new vector which has the modulo value of x from other's x
        and the modulo value of y from other's y.
        Modulates other's x and y values from self's.
        """
        return Vector(self.__x % other.get_x(), self.__y % other.get_y())

    def __rmul__(self, other):
        """
        :param other: scalar to multiply self by
        :return: new vector whose components are other*x and other*y
        Multiplies each component of self by other to create a new vector.
        """
        return Vector(other * self.__x, other * self.__y)

    def __truediv__(self, other):
        """
        :param other: scalar to divide self by
        :return: new vector whose components are x/other and y/other
        Divides each component of self by other to create a new vector.
        """
        return Vector(self.__x / other, self.__y / other)

    def get_distance(self, vector):
        """
        :param vector: vector to calculate the distance from
        :return: the distance between the two vectors.
        """
        return ((self.__x - vector.get_x()) ** 2 +
                (self.__y - vector.get_y()) ** 2) ** 0.5
