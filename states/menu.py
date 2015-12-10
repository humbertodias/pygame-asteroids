# coding: utf-8

"""
The splash screen of the game. The first thing the user sees.
"""

import pygame as pg
import random

from color import *
from asteroid import *

from menu_helper import *
from start_field import *

import state_machine

from virtual_controller import *

class Menu(state_machine._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self, game_controller):
        """
        Construtor
        @param game_controller:
        @return: Instância
        """
        state_machine._State.__init__(self)
        self.game_controller = game_controller
        self.next = "FRANCHISE"
        self.timeout = 10
        self.alpha = 0
        self.alpha_speed = 2  #Alpha change per frame


        self.start_field = StarField(game_controller.screen)

        # criar asteróides aleatoriamente
        nasteroids = random.randint(5,10)
        self.asteroids = game_controller.create_random_asteroids(nasteroids)

        self.title = game_controller.font_large.render(game_controller.game_name, True, Color.WHITE)
        self.bottom = game_controller.font_small.render("Humberto Lino", True, Color.WHITE)
        # Música de fundo
        music = game_controller.asset_manager.play_music('menu.mp3', -1)

        self.xtitle = -self.title.get_width() / 2
        self.ytitle = game_controller.config.height / 4
        self.xtitlefinal = game_controller.config.width / 2 - self.title.get_width() / 2

        self.xbottom = game_controller.config.width - self.bottom.get_width()
        self.ybottom = game_controller.config.height - self.bottom.get_height()

        self.milliseconds = 0

        def call_back_function(sc):

            for a in self.asteroids:
                a.update(4)
                a.draw2(sc)

            if self.xtitle < self.xtitlefinal:
                self.xtitle += 4

            sc.blit(self.title, (self.xtitle, self.ytitle))
            sc.blit(self.bottom, (self.xbottom, self.ybottom))
            self.milliseconds += self.game_controller.clock.tick_busy_loop(game_controller.fps)

            if self.milliseconds > 1000.0*self.timeout:
                self.milliseconds = 0
                self.main_menu.menu.done = True
                self.done = True

            self.start_field.draw()

        self.main_menu = MainMenu(game_controller, call_back_function=call_back_function)

    def update(self, keys, now):
        pass

    def draw(self, surface, interpolate):
        pass

    def get_event(self, event):
        """
        Get events from Control. Changes to next state on any key press.
        """
        pass

    def startup(self, now, persistant):

        """
        Ao iniciar State
        @param now:
        @param persistant:
        """
        self.main_menu.menu.done = False
        self.main_menu.run()

