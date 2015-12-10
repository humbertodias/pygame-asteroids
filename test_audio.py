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
    resource_manager.init_mixer()

    # Carregando
    gameconfig = Game(map)
    gameconfig.width = 640
    gameconfig.height = 480

    screen = pg.display.set_mode((gameconfig.width, gameconfig.height))

    # for music in game_controller.asset_manager.musics:
    #     print(music)
    #     game_controller.asset_manager.play_music(music, 1)


    clock = pg.time.Clock()
    font = resource_manager.get_font()

    sounds = list(resource_manager.sounds.keys())

    index = 0
    done = False
    # Main loop
    while not done:

        time = clock.tick(gameconfig.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                done = True

        index += 1
        if index < len(sounds):

            sound = sounds[index]

            screen.fill((0,0,0))

            text = font.render('ESC para sair', True, Color.GREEN)

            x = (gameconfig.width-text.get_width())/2
            y = (gameconfig.height-text.get_height())/2

            screen.blit(text,(x, y-50))


            text = font.render(sound, True, Color.WHITE)

            x = (gameconfig.width-text.get_width())/2
            y = (gameconfig.height-text.get_height())/2

            screen.blit(text,(x, y))


            # Update the screen.
            pg.display.update()

            resource_manager.play_sound(sound)
            pg.time.delay(1 * 1000)


        else:
            done = True



if __name__ == "__main__":
    main()