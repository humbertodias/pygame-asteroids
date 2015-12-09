import pygame_sdl2 as pg
from ship import *
from color import *
from resource_manager import *

from touch_buttons import *

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

    touch_buttons = TouchButtons(screen, 70)

    done = False
    actions = Game.create_empty_actions()
    while not done:

        time = clock.tick(gameconfig.fps)

        screen.fill(Color.WHITE)

        touch_buttons.draw()

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                done = True

            actions = touch_buttons.detect_actions(event, actions)

        if actions["right"]:
            ship.right(time)
        if actions["left"]:
            ship.left(time)
        if actions["shoot"]:
            ship.shoot()
        if actions["accelerate"]:
            ship.up()

        game_controller.sprites.update(time)
        game_controller.sprites.draw(screen)

        pg.display.update()


if __name__ == "__main__":
    main()