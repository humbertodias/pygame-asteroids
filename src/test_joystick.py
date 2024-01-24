import pygame as pg
import sys
from ship import *
from color import *
from resource_manager import *

from touch_buttons import *

def get_joystick_action(joystick, actions):

    # for i in range(joystick.get_numaxes()):
    #     if joystick.get_axis(i):
    #         print('axis', i)

    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        if joystick.get_button(i):
            print('button', i)

    if buttons >= 14:
        # 7 = left
        if joystick.get_button(7):
            actions['left']=1
        # 5 = right
        if joystick.get_button(5):
            actions['right']=1
        # 15 = Quadrado
        if joystick.get_button(15):
            actions['shoot']=1
        # 14 = X

        if joystick.get_button(14):
            actions['accelerate']=1
    else:

        # 7 = left
        if joystick.get_axis(0) == -1:
            actions['left']=1
        # 5 = right
        if joystick.get_axis(0) >0:
            actions['right']=1
        # 15 = Quadrado
        if joystick.get_button(3):
            actions['shoot']=1

        # 14 = X
        if joystick.get_button(2):
            actions['accelerate']=1


    return actions

def main():
    pg.init()

     # Gerenciador de arquivos
    file_manager = FileManager()
    map = file_manager.load('config.txt')

    # Carregando
    gameconfig = Game(map)


    # Gerenciddos de recurso
    resource_manager = ResourceManager(gameconfig)
    resource_manager.load('resource')


    screen = pg.display.set_mode((gameconfig.width, gameconfig.height))
    game_controller = GameController("Asteroids", screen, file_manager, resource_manager, gameconfig, None)

    game_controller.sprites = SpriteGroup()
    ship = Ship( game_controller.get_display_center(), game_controller, game_controller.sprites)
    game_controller.player = ship
    game_controller.sprites.add(ship)

    clock = pg.time.Clock()


    # Count the joysticks the computer has
    joystick_count = pg.joystick.get_count()
    if joystick_count == 0:
        # No joysticks!
        print("Error, I didn't find any joysticks.")
        sys.exit()
    else:
        # Use joystick #0 and initialize it
        joystick = pg.joystick.Joystick(0)
        joystick.init()

    done = False
    while not done:

        actions = Game.create_empty_actions()
        time = clock.tick(gameconfig.fps)

        screen.fill(Color.WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                done = True

        key = decode_joystick_arrow_to_keyboard_key(joystick)

        if key == pg.K_RIGHT:
            ship.right(time)
        if key == pg.K_LEFT:
            ship.left(time)
        if key == pg.K_SPACE:
            ship.shoot()
        if key == pg.K_UP:
            ship.up()

        game_controller.sprites.update(time)
        game_controller.sprites.draw(screen)

        pg.display.update()


if __name__ == "__main__":
    main()