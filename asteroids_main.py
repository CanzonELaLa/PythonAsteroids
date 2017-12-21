from screen import Screen
import sys
from ship import Ship
from random import randint
from asteroid import Asteroid
from torpedo import Torpedo
from math import cos, sin


DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    CLOCKWISE_ROTATION = 7
    ANTICLOCKWISE_ROTATION = -7
    INITIAL_ASTEROID_SIZE = 3
    INITIAL_TORPEDO_VELOCITY = 0
    ACCELERATION_COEFFICIANT = 2
    COLLISION_MESSAGE = 'You have collided with an asteroid!'
    COLLISION_TITLE = 'Collision!'
    MAX_TORPEDO_LIFE_TIME = 200
    WIN_TITLE = 'Conglaturations'
    WIN_MESSAGE = 'You win!\n The force is strong with this one.'
    LOSE_TITLE = 'all your bases are belong to us'
    LOSE_MESSAGE = 'You lose!\n (I told you though...)'
    QUIT_TITLE = 'Out of witty comebacks exception thrown'
    QUIT_MESSAGE = "You quit!\n Can't say I blame you"


    def __init__(self, asteroids_amnt):
        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        location = [randint(self.screen_min_x, self.screen_max_x),
                    randint(self.screen_min_y, self.screen_max_y)]
        self.__ship = Ship(location, [0, 0], 0)
        self.__max_delta_x = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
        self.__max_delta_y = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y
        self.__asteroids = []
        self.__create_asteroids(asteroids_amnt)
        self.__torpedoes = []
        self.__score = 0

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
        Your code goes here!
        """
        quit = False
        message = ""
        title = ""
        if len(self.__asteroids) == 0:
            title = self.WIN_TITLE
            message = self.WIN_MESSAGE
            quit = True
        elif self.__ship.get_lives() == 0:
            title = self.LOSE_TITLE
            message = self.LOSE_MESSAGE
            quit = True
        elif self._screen.should_end():
            title = self.QUIT_TITLE
            message = self.QUIT_MESSAGE
            quit = True
        if quit:
            self.__game_over(message, title)

        if self._screen.is_left_pressed():
            self.__ship.rotate(self.CLOCKWISE_ROTATION)
        if self._screen.is_right_pressed():
            self.__ship.rotate(self.ANTICLOCKWISE_ROTATION)
        if self._screen.is_up_pressed():
            self.__ship.accelerate()
        if self._screen.is_space_pressed():
            self.__shoot_torpedo()

        self.update_locations()

        self.__remove_old_torpedoes()

        if self.__check_collisions_with_ship():
            self._screen.show_message(self.COLLISION_TITLE,
                                      self.COLLISION_MESSAGE)
            self.__ship.subtract_life()
            self._screen.remove_life()

        self.__torpedo_hit()

    def __game_over(self, message, title):
        self._screen.show_message(title, message)

        self._screen.end_game()
        sys.exit()

    def update_locations(self):
        self.move_ship()
        self.move_asteroids()
        self.move_torpedoes()

    def __remove_old_torpedoes(self):
        torpedoes_to_remove = []

        for torpedo in self.__torpedoes:
            if torpedo.get_life_time() >= self.MAX_TORPEDO_LIFE_TIME:
                torpedoes_to_remove.append(torpedo)

        for torpedo in torpedoes_to_remove:
            self.__torpedoes.remove(torpedo)
            self._screen.unregister_torpedo(torpedo)

    def __shoot_torpedo(self):
        if len(self.__torpedoes) < 15:
            torpedo = Torpedo(self.__ship.get_location(),
                              self.__get_torpedo_speed(),
                              self.__ship.get_heading())
            self._screen.register_torpedo(torpedo)
            self.__torpedoes.append(torpedo)

    def __get_torpedo_speed(self):
        return [self.__ship.get_velocity_x() + self.ACCELERATION_COEFFICIANT
                * cos(self.__ship.get_rad_heading()),
                self.__ship.get_velocity_y() + self.ACCELERATION_COEFFICIANT
                * sin(self.__ship.get_rad_heading())]

    def __check_collisions_with_ship(self):
        is_collision = False
        i = 0
        while i < len(self.__asteroids):
            if self.__asteroids[i].has_intersection(self.__ship):
                is_collision = True
                self._screen.unregister_asteroid(self.__asteroids[i])
                self.__asteroids.remove(self.__asteroids[i])
            else:
                i += 1

        return is_collision

    def __torpedo_hit(self):
        # Using while loop because changes to the lists happen
        asteroids_to_remove = []
        torpedoes_to_remove = []

        for asteroid in self.__asteroids:
            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    self.__blow_up_asteroid(asteroid, torpedo)
                    torpedoes_to_remove.append(torpedo)
                    asteroids_to_remove.append(asteroid)
                    break  # Current torpedo expended

        for torpedo in torpedoes_to_remove:
            self._screen.unregister_torpedo(torpedo)
            self.__torpedoes.remove(torpedo)

        for asteroid in asteroids_to_remove:
            self._screen.unregister_asteroid(asteroid)
            self.__asteroids.remove(asteroid)

    def __blow_up_asteroid(self, asteroid, torpedo):
        size = asteroid.get_size()
        self.__score += self.__calc_asteroid_score(size)
        self._screen.set_score(self.__score)

        if size > 1:
            asteroid_vel = asteroid.get_velocity()
            torpedo_vel = torpedo.get_velocity()
            asteroid_speed = (asteroid_vel[0] ** 2 + asteroid_vel[1] ** 2) ** \
                             0.5
            velocity_x = (torpedo_vel[0] + asteroid_vel[0]) / asteroid_speed
            velocity_y = (torpedo_vel[1] + asteroid_vel[1]) / asteroid_speed
            new_asteroids = [Asteroid(asteroid.get_location(),
                                      [velocity_x, velocity_y], size - 1),
                             Asteroid(asteroid.get_location(),
                                      [-velocity_x, -velocity_y], size - 1)]
            self.__asteroids += new_asteroids
            for new_asteroid in new_asteroids:
                self._screen.register_asteroid(new_asteroid,
                                               new_asteroid.get_size())

    # todo:: move to asteroid.py
    @staticmethod
    def __calc_asteroid_score(size):
        if size == 3:
            return 20
        elif size == 2:
            return 50
        elif size == 1:
            return 100

    def __create_asteroids(self, amount):
        i = 0
        while i < amount:
            pos_x = randint(self.screen_min_x, self.screen_max_x)
            pos_y = randint(self.screen_min_y, self.screen_max_y)
            vel_x = randint(1, 7)
            vel_y = randint(1, 7)

            if self.__ship.get_location() != [pos_x, pos_y]:
                asteroid = Asteroid([pos_x, pos_y], [vel_x, vel_y],
                                    self.INITIAL_ASTEROID_SIZE)
                self.__asteroids.append(asteroid)
                self._screen.register_asteroid(asteroid, asteroid.get_size())
                i += 1

    def move_asteroids(self):
        for asteroid in self.__asteroids:
            self.move_object(asteroid)
            self._screen.draw_asteroid(asteroid, asteroid.get_position_x(),
                                       asteroid.get_position_y())

    def move_torpedoes(self):
        for torpedo in self.__torpedoes:
            torpedo.add_life_time()
            self.move_object(torpedo)
            self._screen.draw_torpedo(torpedo, torpedo.get_position_x(),
                                      torpedo.get_position_y(),
                                      torpedo.get_heading())

    def move_ship(self):
        self.move_object(self.__ship)

        self._screen.draw_ship(self.__ship.get_position_x(),
                               self.__ship.get_position_y(),
                               self.__ship.get_heading())

    def move_object(self, obj):
        obj.set_position_x((obj.get_velocity_x() + obj.get_position_x() -
                            self.screen_min_x) % self.__max_delta_x +
                           self.screen_min_x)
        obj.set_position_y((obj.get_velocity_y() + obj.get_position_y() -
                            self.screen_min_y) % self.__max_delta_y +
                           self.screen_min_y)


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
