# coding: utf-8

"""
Tela como selo de classificação do jogo.
Segunda coisa que o jogador visualiza.
"""

import pygame_sdl2 as pg
from resource import *
from color import *
from font import *

import state_machine
from polygon import *
from virtual_controller import *


class Franchise(state_machine._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self, game_controller):
        state_machine._State.__init__(self)
        self.game_controller = game_controller
        self.next = "SEAL"
        self.timeout = 10
        self.alpha = 0
        self.alpha_speed  = 2  #Alpha change per frame
        # self.image = game_controller.asset_manager.get_image('esrb_everyone.png').copy().convert()
        # self.image.set_alpha(self.alpha)
        # self.rect = self.image.get_rect(center=self.game_controller.screen_rect().center)
        self.font = game_controller.asset_manager.get_font(Font.LARGE)
        self.text=self.font.render("Polygon Games", True, Color.WHITE)

        self.cube = Cube()

    def update(self, keys, now):
        """Updates the splash screen."""
        self.now = now
        self.alpha = min(self.alpha+self.alpha_speed, 255)
        # self.image.set_alpha(self.alpha)
        if self.now-self.start_time > 1000.0*self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        surface.fill(Color.BLACK)
        self.cube.draw(surface)
        surface.blit(self.text, (self.game_controller.width/2 - self.text.get_width()/2, self.game_controller.height - self.text.get_height()))

    def get_event(self, event):
        """
        Get events from Control. Changes to next state on any key press.
        """
        self.done = is_event_type_an_input_down(event)
