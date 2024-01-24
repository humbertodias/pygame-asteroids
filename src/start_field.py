import pygame as pg
import random


class StarField(object):

    # Constants
    NUM_STARS = 30
    WHITE = 255, 255, 255
    LEFT = 0
    RIGHT = 1

    # Simulation variables.
    direction = LEFT
    stars = []

    def __init__(self, screen):
        "Create the starfield"
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # The starfield is represented as a dictionary of x and y values.
        stars = []

        # Create a list of (x,y) coordinates.
        for loop in range(0, self.NUM_STARS):
            star = [random.randrange(0, self.width),
                    random.randrange(0, self.height)]
            stars.append(star);

        self.stars = stars

    def move(self, start, end, direction):
        "Correct for stars hitting the screen's borders"

        for loop in range(start, end):
            if (direction == self.LEFT):
                if (self.stars[loop][0] != 1):
                    self.stars[loop][0] = self.stars[loop][0] - 1
                else:
                    self.stars[loop][0] = self.screen.get_width() - 1
                    self.stars[loop][1] = random.randrange(0, self.height - 1)
            elif (direction == self.RIGHT):
                if (self.stars[loop][0] != self.width - 1):
                    self.stars[loop][0] = self.stars[loop][0] + 1
                else:
                    self.stars[loop][0] = 1
                    self.stars[loop][1] = random.randrange(0, self.height - 1)

            self.stars[loop] = self.fix_stars_on_screen(self.stars[loop])

    def fix_stars_on_screen(self, star):
        # fix
        if star[0] <= 0 : star[0] = 1
        if star[1] <= 0 : star[1] = 1
        if star[0] >= self.width: star[0] = self.width-1
        if star[1] >= self.height: star[1] = self.height-1

        return star

    def draw(self):
        # Check if first field's stars hit the screen border.
        self.move(0, 10, self.direction)

        # Place ten white stars.
        for loop in range(0, self.NUM_STARS):
            self.screen.set_at(self.stars[loop], self.WHITE)
