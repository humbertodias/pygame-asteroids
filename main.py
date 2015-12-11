# coding: utf-8

__author__  = 'Humberto Lino'
__version__ = '1.0'

import sys
import pygame as pg


from resource_manager import *
from font import *
from game import *
from score import *
from file import *

import tools

from states.seal import *
from states.franchise import *
from states.intro import *
from states.menu import *



def main():
    """
    Método principal, que inicializa o jogo
    """

    # Definições
    game_name = 'Asteróides'
    score_file_name = 'score.dat'
    config_file_name = 'config.txt'
    resource_dir_name = 'resource'

    # nao informou o nome do arquivo
    if len(sys.argv) > 2:
        config_file_name = sys.argv[1]

    if not os.path.isfile(config_file_name):
        print('python main.py NOME_DO_ARQUIVO_DE_CONFIGURACAO.txt')
        exit(-1)

    # inicializa pygame
    pg.init()

    # Gerenciador de arquivos
    file_manager = FileManager()
    map = file_manager.load(config_file_name)

    # Gerenciddos de recurso
    resource_manager = ResourceManager()
    resource_manager.load(resource_dir_name)

    # Título e ícone
    # pg.display.set_caption(game_name)
    pg.display.set_icon(resource_manager.get_image('icon.png'))

    # Carregando
    scoredat = file_manager.unmarshal_marshal(score_file_name, DataHandler().defaultscore())
    gameconfig = Game(map)

    pg.mouse.set_visible(gameconfig.show_mouse)

    colors = 16
    flag = pg.HWSURFACE|pg.DOUBLEBUF
    if gameconfig.full_screen:
        flag = pg.FULLSCREEN

    screen = pg.display.set_mode((gameconfig.width, gameconfig.height), flag, colors)
    game_controller = GameController(game_name, screen, file_manager, resource_manager, gameconfig, scoredat)

    game_controller.asset_manager.init_mixer()

    # Máquina de estado
    app = tools.Control(game_name, gameconfig.fps)
    state_dict = {"FRANCHISE"   : Franchise(game_controller),
                  "SEAL"   : Seal(game_controller),
                  "INTRO"  : Introduction(game_controller),
                  "MENU"   : Menu(game_controller)
                  }
    app.state_machine.setup_states(state_dict, "FRANCHISE")

    # guardar maquina de estado no controlador
    game_controller.app = app

    app.main()

if __name__ == "__main__":
    main()


