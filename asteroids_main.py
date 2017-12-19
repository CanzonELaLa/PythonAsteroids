from screen import Screen
import sys
from ship import Ship
from random import randint
from asteroid import Asteroid

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amnt):
        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        location = [randint(self.screen_min_x, self.screen_max_x),
                    randint(self.screen_min_y, self.screen_max_y)]
        self.__ship = Ship(location, [0, 0], 0)

        # TODO:: Make sure randomized positions of asteroids are not the
        # TODO:: same as the ship
        self.__asteroids = [Asteroid(
            [randint(self.screen_min_x, self.screen_max_x),
             randint(self.screen_min_y, self.screen_max_y)],
            [randint(self.screen_min_x, self.screen_max_x),
             randint(self.screen_min_y, self.screen_max_y)], 3)
            for _ in range(asteroids_amnt)]

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
        '''
        Your code goes here!
        '''
        Screen.draw_ship(self.__ship.get_position_x(),
                         self.__ship.get_position_y(),
                         self.__ship.get_heading())

        for asteroid in self.__asteroids:
            Screen.draw_asteroid(asteroid, asteroid.get_position_x(),
                                 asteroid.get_position_y())


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
