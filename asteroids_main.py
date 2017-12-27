from screen import Screen
import sys
from ship import Ship
from random import randint, choice
from asteroid import Asteroid
from torpedo import Torpedo
from vector import Vector
from math import cos, sin

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    # ship related constants
    SHIP_ROTATION_INCREMENT = 7

    # asteroids related constants
    NEW_ASTEROIDS_AMOUNT = 2  # amount of asteroids split from original
    MIN_ASTEROID_VELOCITY = 1
    MAX_ASTEROID_VELOCITY = 7

    # torpedo related constants
    TORPEDO_ACCELERATION_COEFFICIENT = 2
    MAX_TORPEDO_LIFE_CYCLES = 200
    MAX_ACTIVE_TORPEDOES = 15

    # game messages
    COLLISION_MESSAGE = 'You have collided with an asteroid!'
    COLLISION_TITLE = 'Collision!'

    WIN_TITLE = 'Conglaturations'
    WIN_MESSAGE = 'You win!\n The force is strong with this one.'

    LOSE_TITLE = 'all your bases are belong to us'
    LOSE_MESSAGE = 'You lose!\n (I told you though...)'

    QUIT_TITLE = 'OutOfWittyComebacksException thrown'
    QUIT_MESSAGE = "You quit!\n Can't say I blame you"

    def __init__(self, asteroids_amnt):
        """
        :param asteroids_amnt: amount of asteroid to be spawned at the
        beginning of the game.
        creates and instance of an Asteroids game
        """

        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y

        # create ship at random starting location withing screen boundaries
        location = Vector(randint(self.screen_min_x, self.screen_max_x),
                          randint(self.screen_min_y, self.screen_max_y))

        # saves ship object, asteroids list, torpedoes list and score as
        # GameRunner members
        self.__ship = Ship(location)
        self.__asteroids = []
        self.__create_asteroids(asteroids_amnt)
        self.__torpedoes = []
        self.__score = 0

    def __create_asteroids(self, amount):
        """
        :param amount: amount of asteroids to create.
        Creates asteroids in random locations and random velocities where
        each location will differ from ship location and velocities will
        range from -MAX_VELOCITY to -MIN_VELOCITY or MIN_VELOCITY to
        MAX_VELOCITY
        """
        ship_x = self.__ship.get_location().get_x()
        ship_y = self.__ship.get_location().get_y()

        # creates list of possible velocities
        velocity_range = list(range(-self.MAX_ASTEROID_VELOCITY,
                                    -self.MIN_ASTEROID_VELOCITY)) \
                         + list(range(self.MIN_ASTEROID_VELOCITY,
                                      self.MAX_ASTEROID_VELOCITY))

        for i in range(amount):

            # generates random x coordinate for asteroid
            asteroid_x = randint(self.screen_min_x, self.screen_max_x)
            if asteroid_x == ship_x:

                # if asteroid has same x coordinate as ship, generates a y
                # coordinate different from the ship's so they don't spawn on
                # the same spot
                rand = randint(self.screen_min_y, self.screen_max_y - 1)
                asteroid_y = rand + (1 if rand >= ship_y else 0)
            else:
                asteroid_y = randint(self.screen_min_y, self.screen_max_y)

            location = Vector(asteroid_x, asteroid_y)

            # generates random velocity for asteroid such that the speed
            # will not be 0 in each axis
            velocity = Vector(choice(velocity_range), choice(velocity_range))

            # creates asteroid object, adds it game asteroid list member
            # and registers it on screen object
            asteroid = Asteroid(location, velocity, Asteroid.BIG_ASTEROID_SIZE)
            self.__asteroids.append(asteroid)
            self._screen.register_asteroid(asteroid, asteroid.get_size())

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        runs game instance
        """

        game_over_flag = False
        message = ""
        title = ""

        # if there are no asteroid left in the game, player wins
        if len(self.__asteroids) == 0:
            title = self.WIN_TITLE
            message = self.WIN_MESSAGE
            game_over_flag = True

        # if there are no lives left, player loses
        elif self.__ship.get_lives() == 0:
            title = self.LOSE_TITLE
            message = self.LOSE_MESSAGE
            game_over_flag = True

        # if quit button was pushed, ends game
        elif self._screen.should_end():
            title = self.QUIT_TITLE
            message = self.QUIT_MESSAGE
            game_over_flag = True

        # if any of the above is True, shows proper message
        if game_over_flag:
            self.__game_over(message, title)

        # rotates ship according to pressed key (left/right)
        if self._screen.is_left_pressed():
            self.__ship.rotate(self.SHIP_ROTATION_INCREMENT)
        if self._screen.is_right_pressed():
            self.__ship.rotate(-self.SHIP_ROTATION_INCREMENT)

        # accelerates ship if up is pressed
        if self._screen.is_up_pressed():
            self.__ship.accelerate()

        # shoots torpedo if space is pressed
        if self._screen.is_space_pressed():
            self.__shoot_torpedo()

        # update locations for ship, asteroids and torpedoes
        self.update_locations()

        # remove torpedoes that timed out
        self.__remove_old_torpedoes()

        # if ship has collided with an asteroid show message and subtract life
        if self.__check_collisions_with_ship():
            self._screen.show_message(self.COLLISION_TITLE,
                                      self.COLLISION_MESSAGE)
            self.__ship.subtract_life()
            self._screen.remove_life()

        self.__torpedo_hit()

    def __game_over(self, title, message):
        """
        :param title: the title of the message to be shown to the user
        :param message: the message to be shown to the user
        shows game over message and ends the game
        """

        self._screen.show_message(title, message)
        self._screen.end_game()
        sys.exit()

    def __shoot_torpedo(self):
        """
        shoots new torpedo if there are less than the max active torpedoes
        in the game
        """

        if len(self.__torpedoes) < self.MAX_ACTIVE_TORPEDOES:
            torpedo = Torpedo(self.__ship.get_location().get_copy(),
                              self.__get_torpedo_velocity(),
                              self.__ship.get_heading())
            self._screen.register_torpedo(torpedo)
            self.__torpedoes.append(torpedo)

    def __get_torpedo_velocity(self):
        """
        calculates torpedo velocity based on ship velocity, heading and
        the game's torpedo acceleration coefficient
        """

        return (self.__ship.get_velocity() +
                self.TORPEDO_ACCELERATION_COEFFICIENT *
                Vector(cos(self.__ship.get_rad_heading()),
                       sin(self.__ship.get_rad_heading())))

    def update_locations(self):
        """
        updates ship, asteroids and torpedoes location
        """

        self.move_ship()
        self.move_asteroids()
        self.move_torpedoes()

    def move_ship(self):
        """
        updates ship location and draws ship at new location on screen
        """
        self.move_object(self.__ship)

        self._screen.draw_ship(self.__ship.get_location().get_x(),
                               self.__ship.get_location().get_y(),
                               self.__ship.get_heading())

    def move_asteroids(self):
        """
        updates asteroids location and draws them on screen
        """

        for asteroid in self.__asteroids:
            self.move_object(asteroid)
            self._screen.draw_asteroid(asteroid,
                                       asteroid.get_location().get_x(),
                                       asteroid.get_location().get_y())

    def move_torpedoes(self):
        """
        updates torpedo life time, location and draws them on screen
        """

        for torpedo in self.__torpedoes:
            torpedo.add_life_cycle()
            self.move_object(torpedo)
            self._screen.draw_torpedo(torpedo,
                                      torpedo.get_location().get_x(),
                                      torpedo.get_location().get_y(),
                                      torpedo.get_heading())

    def move_object(self, obj):
        """
        :param obj: object whose location is to be updated
        updates object location based on current velocity and location
        """

        # gets object location and velocity
        obj_location = obj.get_location()
        obj_velocity = obj.get_velocity()

        delta_vector = Vector(self.screen_max_x - self.screen_min_x,
                              self.screen_max_y - self.screen_min_y)

        min_vector = Vector(self.screen_min_x, self.screen_min_y)

        # calculates and sets new object location based on current location
        # and velocity
        obj.set_location((obj_velocity + obj_location - min_vector) %
                         delta_vector + min_vector)

    def __remove_old_torpedoes(self):
        """
        removes all torpedoes who are past their max life cycles for the game
        from the game
        """

        # builds a list of torpedoes to remove
        torpedoes_to_remove = []

        for torpedo in self.__torpedoes:
            if torpedo.get_life_cycle() >= self.MAX_TORPEDO_LIFE_CYCLES:
                torpedoes_to_remove.append(torpedo)

        # removes each torpedo in list from screen and game instance
        for torpedo in torpedoes_to_remove:
            self._screen.unregister_torpedo(torpedo)
            self.__torpedoes.remove(torpedo)

    def __check_collisions_with_ship(self):
        """
        check is ship has collided with an asteroid. If so, removes said
        asteroid from screen and game instance and returns True.
        Otherwise, returns False.
        """

        # initializes collision flag to False
        is_collision = False

        i = 0
        while i < len(self.__asteroids):

            # if asteroid i intersects with the ship, collision flag is set
            # to True, and asteroid is removed from screen and game instance
            if self.__asteroids[i].has_intersection(self.__ship):

                is_collision = True

                self._screen.unregister_asteroid(self.__asteroids[i])
                self.__asteroids.remove(self.__asteroids[i])
            else:
                # if no asteroid was removed, move to next asteroid in list
                i += 1

        return is_collision

    def __torpedo_hit(self):
        """
        removes torpedoes and asteroids that have collided from screen and
        game instance
        """
        # Using while loop because changes to the lists happen
        asteroids_to_remove = []
        torpedoes_to_remove = []

        for asteroid in self.__asteroids:
            for torpedo in self.__torpedoes:
                # if asteroid i intersects with torpedo j, blows up asteroid i
                # (including score update and smaller asteroids spawning in
                # its place), and adds torpedo j and asteroid i to their
                # appropriate lists, so they can be removed
                if asteroid.has_intersection(torpedo):
                    self.__handle_hit_asteroid(asteroid, torpedo)
                    torpedoes_to_remove.append(torpedo)
                    asteroids_to_remove.append(asteroid)
                    break  # Current torpedo expended

        # removes each torpedo and asteroid in list from screen and game
        # instance
        for torpedo in torpedoes_to_remove:
            self._screen.unregister_torpedo(torpedo)
            self.__torpedoes.remove(torpedo)

        for asteroid in asteroids_to_remove:
            self._screen.unregister_asteroid(asteroid)
            self.__asteroids.remove(asteroid)

    def __handle_hit_asteroid(self, asteroid, torpedo):
        """
        :param asteroid: the asteroid that was hit
        :param torpedo: the torpedo that hit the asteroid
        updates score, and splits asteroid into smaller asteroids if necessary
        """

        # updates game score according to asteroid size
        self.__score += asteroid.get_score()
        self._screen.set_score(self.__score)

        # if asteroid size is larger than small, split asteroid into smaller
        # asteroids
        if asteroid.get_size() > Asteroid.SMALL_ASTEROID_SIZE:

            asteroid_vel = asteroid.get_velocity()
            torpedo_vel = torpedo.get_velocity()

            asteroid_speed = asteroid_vel.get_size()

            # calculates new asteroids velocity
            new_asteroid_vel = (torpedo_vel + asteroid_vel) / asteroid_speed

            # creates new asteroids, with each asteroid going in the opposite
            # direction of the previous, and adds them to screen and game
            # instance
            for i in range(self.NEW_ASTEROIDS_AMOUNT):
                new_asteroid = Asteroid(asteroid.get_location().get_copy(),
                                        (-1 if i % 2 == 1 else 1)
                                        * new_asteroid_vel,
                                        asteroid.get_size() - 1)
                self.__asteroids.append(new_asteroid)
                self._screen.register_asteroid(new_asteroid,
                                               new_asteroid.get_size())


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
