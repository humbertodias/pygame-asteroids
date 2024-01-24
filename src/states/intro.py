# coding: utf-8

"""
Tela inicial do jogo.
Primeira coisa que o jogador visualiza.
"""

import pygame as pg

from color import *
from font import *
import credit

import state_machine
from virtual_controller import *

class Introduction(state_machine._State):
    """This State is updated while our game shows the splash screen."""

    def __init__(self, game_controller):
        state_machine._State.__init__(self)
        self.game_controller = game_controller
        self.next = "MENU"
        self.timeout = 0

        print(self.game_controller.width)

        if self.game_controller.width <= 800:
            font_size = Font.SMALL
        else:
            font_size = Font.NORMAL

        self.font = game_controller.asset_manager.get_font(font_size)
        self.image = game_controller.asset_manager.get_scalled_image('splash.png', 0.25)


    def update(self, keys, now):
        """Updates the splash screen."""
        self.now = now
        if self.now-self.start_time > 1000.0*self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        pass

    def get_event(self, event):
        """
        Get events from Control. Changes to next state on any key press.
        """
        self.done = is_event_type_an_input_down(event)


    def startup(self, now, persistant):
        self.game_controller.screen.fill(Color.BLACK)

        def callback(sc):
            sc.blit(self.image, (0,0))

        credit.credit_from_file('resource/text/intro.txt',self.font, Color.WHITE, 15, callback)
