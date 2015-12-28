import pygame as pg

from game import *

class TouchButtons:

    def __init__(self, screen, resource_manager, button_width = 40):
        self.screen = screen
        self.resource_manager = resource_manager
        self.size = (pg.display.Info().current_w, pg.display.Info().current_h)
        self.create_touch_buttons(button_width)


    def create_touch_buttons(self, button_width):
        ## Create rectangles that will detect direction
        self.left = self.resource_manager.get_image('left.png').convert_alpha()
        # self.left = pg.transform.scale(self.left, (button_width, button_width))

        self.right = self.resource_manager.get_image('right.png').convert_alpha()
        # self.right = pg.transform.scale(self.right, (button_width, button_width))

        self.power = self.resource_manager.get_image('power.png').convert_alpha()
        # self.power = pg.transform.scale(self.power, (button_width, button_width))

        self.shot = self.resource_manager.get_image('shot.png').convert_alpha()
        # self.shot = pg.transform.scale(self.shot, (button_width, button_width))

        self.left_rect = pg.Rect(0, self.size[1]-button_width, button_width, button_width)
        self.right_rect = pg.Rect(button_width, self.size[1]-button_width, button_width, button_width)

        self.shot_rect = pg.Rect(self.size[0]-button_width, self.size[1]-button_width, button_width, button_width)
        self.power_rect = pg.Rect(self.size[0]-button_width*2, self.size[1]-button_width, button_width, button_width)

    def draw(self):
        ## draw the rectangles that will detect direction
        self.screen.blit(self.left, self.left_rect)
        self.screen.blit(self.right, self.right_rect)
        self.screen.blit(self.shot, self.shot_rect)
        self.screen.blit(self.power, self.power_rect)


    def detect_actions(self, event, actions):
        ## Check to see if the mousebutton is pressed

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            ## Check if the mouse_pos is within the rectangle
            if self.left_rect.collidepoint(mouse_pos):
                actions["left"]=1
            if self.right_rect.collidepoint(mouse_pos):
                actions["right"]=1
            if self.power_rect.collidepoint(mouse_pos):
                actions["accelerate"]=1
            if self.shot_rect.collidepoint(mouse_pos):
                actions["shoot"]=1
        if event.type == pg.MOUSEBUTTONUP:
            actions = Game.create_empty_actions()

        return actions

