# coding: utf-8

import pygame_sdl2 as pg
import math, random

from sprite_collision import *
from color import *


class Asteroid(SpriteCollision,pg.sprite.Sprite):
    """
    Representa o asteroid
    """

    SPEED = 0.5
    """
    Velocidade do asteroide
    """

    SECTIONS = 2
    """
    Secções, ou partes que o asteroide será dividido ao ser atingido
    """

    def __init__(self, location, size, angle, game_controller
                 , from_color = Color.PINK
                 , to_color = (255,0,0,255)
                 , *groups):
        """
        Construtor
        """

        super(Asteroid,self).__init__(*groups)

        self.location = location
        self.from_color = from_color
        self.to_color = to_color
        self.game_controller = game_controller
        self.original_image = game_controller.asset_manager.get_image("asteroid.png").convert_alpha()
        self.scale(size)
        self.original_image = Color.color_replace(self.original_image, from_color, to_color )

        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        center_position = [ location[0] + self.original_image.get_width()/2
                          , location[1] + self.original_image.get_height()/2
                          ]
        self.rect.center = center_position


        self.angle = angle
        self.rotate()

        realangle=math.radians(self.angle)

        # asteroids maiores sao mais lentos
        self.SPEED = (self.SPEED / size)

        self.initrect(location, self.game_controller)


        if location[0]<= 1:
            self.rect.right=location[0]
        elif location[0]>= game_controller.width:
            self.rect.left=location[0]
        else:
            self.rect.centerx=location[0]
        if location[1]<= 1:
            self.rect.bottom=location[1]
        elif location[1]>= game_controller.height:
            self.rect.top=location[1]
        else:
            self.rect.centery==location[1]

        self.speedx=(random.randrange(1)*2-1)*((random.randrange(70)+5))/(80 + 30 * size) * math.cos(realangle)
        self.speedy=(random.randrange(1)*2-1)*((random.randrange(70)+5))/(80 + 30 * size) * math.sin(realangle)
        if self.speedx <- self.SPEED:
            self.speedx=- self.SPEED
        if self.speedx > self.SPEED:
            self.speedx=self.SPEED
        if self.speedy < -self.SPEED:
            self.speedy=-self.SPEED
        if self.speedy > self.SPEED:
            self.speedy = self.SPEED
        (self.x,self.y)=self.rect.center
        self.size=size

    def scale(self, size):
        width,height = self.original_image.get_width() * size, self.original_image.get_height() * size
        self.original_image = pg.transform.scale(self.original_image, (width, height))

    def rotate(self):
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect  = self.image.get_rect()
        self.rect.center = old_center


    def random_angle(self):
        """
        Retorna angulo aleatória
        """
        return random.randrange(359)+1

    def destroy(self, angle):
        """
        Destruir asteroids
        @param angle: Ângulo
        """

        # > 1. Divida-o
        if self.size > 1:

            for object in range(0, self.SECTIONS):
                Asteroid((self.rect.x+random.randrange(self.image.get_width()-30)+30,self.rect.y+random.randrange(self.image.get_height()-30)+30)
                         ,self.size-1
                         ,self.random_angle()
                         ,self.game_controller
                         ,self.from_color
                         ,self.to_color
                         ,self.game_controller.sprites
                         ,self.game_controller.asteroids)

            self.game_controller.score+=15/self.size
            self.game_controller.asset_manager.play_sound('hit_hurt.wav')
        else:
            self.game_controller.score+=5/self.size

        self.kill()

    def update(self,time):
        """
        Atualizar
        @param time: Delta Time
        """
        if self.game_controller.running and not self.game_controller.gameover:
            if self.collision(self.game_controller.player) and self.game_controller.player.invincibility<=0.0:
                self.destroy( self.random_angle() )
                self.game_controller.player.explode(time)


        self.x+=0.5*time*self.speedx/(self.size+1)
        self.y+=0.5*time*self.speedy/(self.size+1)
        self.rect.center=(self.x,self.y)
        self.screencollision(time)
