import pygame as pg
from start_field import *

def main():

    pg.init()
    screen = pg.display.set_mode((1024, 762))

    # Create the starfield.
    star_field = StarField(screen)

    clock = pg.time.Clock()

    # Main loop
    while 1:

        # Handle input events.
        event = pg.event.poll()
        if (event.type == pg.QUIT):
            break
        elif (event.type == pg.KEYDOWN):
            if (event.key == pg.K_ESCAPE):
                break

        screen.fill((0,0,0))
        star_field.draw()

        # Update the screen.
        pg.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main()