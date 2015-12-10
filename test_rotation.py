import pygame as pg
from ship import *
from file import *
from resource_manager import *
from game import *


def main():

    pg.init()

     # Gerenciador de arquivos
    file_manager = FileManager()
    map = file_manager.load('entrada.txt')

    # Gerenciddos de recurso
    resource_manager = ResourceManager()
    resource_manager.load('resource')

    # Carregando
    gameconfig = Game(map)

    screen = pg.display.set_mode((gameconfig.width, gameconfig.height))
    game_controller = GameController("Asteroids", screen, file_manager, resource_manager, gameconfig, None)

    game_controller.sprites = SpriteGroup()
    ship = Ship( game_controller.get_display_center(), game_controller, game_controller.sprites)
    game_controller.player = ship
    game_controller.sprites.add(ship)

    clock = pg.time.Clock()

    # Main loop
    while 1:

        time = clock.tick(gameconfig.fps)

        # Handle input events.
        event = pg.event.poll()
        if event.type == pg.QUIT:
            break
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                break

        key=pg.key.get_pressed()
        if key[pg.K_LEFT]:
            ship.left(time)
        if key[pg.K_RIGHT]:
            ship.right(time)
        if key[pg.K_UP]:
            ship.up()
        if key[pg.K_SPACE]:
            ship.shoot()

        screen.fill((0,0,0))
        game_controller.sprites.update(time)
        game_controller.sprites.draw(screen)

        # Update the screen.
        pg.display.update()

if __name__ == "__main__":
    main()