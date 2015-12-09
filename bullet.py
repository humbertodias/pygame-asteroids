# coding: utf-8

import pygame_sdl2 as pg
import math

from sprite_collision import *

class Bullet(SpriteCollision, pg.sprite.Sprite):
    """
    Bala
    """

    def __init__(self,location,angle,game_controller, *groups):
        """
        Construtor
        @param location:
        @param angle:
        @param game_controller:
        @param groups:
        @return: Instância
        """
        super(Bullet,self).__init__(*groups)
        self.game_controller = game_controller
        self.image = game_controller.asset_manager.get_image("bullet.png").convert_alpha()
        self.rect=pg.rect.Rect(location,self.image.get_size())

        if angle+90>360:
            angle-=360.0
        self.realangle = math.radians(angle+90)
        self.rect.center=location
        self.speedx = +1.0 * math.cos(self.realangle)
        self.speedy = -1.0 * math.sin(self.realangle)
        self.timer=250.0
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        (self.x,self.y)=self.rect.center
        self.initrect(location, self.game_controller)

    def update(self,time):
        """
        Atualizar
        @param time:  Delta time
        """
        self.timer-=time
        self.x+=self.speedx*time
        self.y+=self.speedy*time
        self.rect.center=(self.x,self.y)

        # 8x8
        sz = self.image.get_width()
        if self.rect.left>self.game_controller.width - sz:
            self.rect.right=sz
            self.destroy()
        if self.rect.top>self.game_controller.height - sz:
            self.rect.bottom=sz
            self.destroy()
        if self.rect.right<sz:
            self.rect.left= self.game_controller.width - sz
            self.destroy()
        if self.rect.bottom<sz:
            self.rect.top= self.game_controller.height - sz
            self.destroy()

        for object in self.game_controller.sprites.sprites():
            if self.game_controller.player!= object and self!=object:
                if self.collision(object):
                    object.destroy(self.realangle)
                    self.kill()
                    break

        self.screencollision(time)

    def destroy(self):
        """
        Destruir
        """
        self.kill()
